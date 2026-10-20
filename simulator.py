from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path

from .risk import RiskConfig, position_notional
from .strategy import Bar, crossover_signal


@dataclass
class Trade:
    timestamp: int
    side: str
    price: float
    quantity: float
    fee: float
    realized_pnl: float
    equity: float


def synthetic_bars(count: int, seed: int = 7) -> list[Bar]:
    if count < 1:
        raise ValueError("bars must be positive")
    rng = random.Random(seed)
    price = 100.0
    result = []
    for t in range(count):
        drift = 0.00015 if (t // 90) % 2 == 0 else -0.00008
        price *= math.exp(drift + rng.gauss(0, 0.006))
        result.append(Bar(t, price))
    return result


def run_simulation(bars: list[Bar], initial_equity: float = 10_000.0,
                   fee_rate: float = 0.0005, slippage: float = 0.0002,
                   config: RiskConfig | None = None) -> tuple[list[Trade], dict]:
    config = config or RiskConfig()
    config.validate()
    if initial_equity <= 0 or fee_rate < 0 or slippage < 0:
        raise ValueError("invalid simulation settings")
    equity = initial_equity
    position = 0.0
    entry = 0.0
    trades: list[Trade] = []
    history: list[Bar] = []
    peak = equity
    max_drawdown = 0.0
    for bar in bars:
        history.append(bar)
        target = crossover_signal(history)
        desired = target * position_notional(equity, bar.close, config) / bar.close
        delta = desired - position
        if abs(delta) < 1e-12:
            peak = max(peak, equity)
            max_drawdown = max(max_drawdown, (peak - equity) / peak)
            continue
        fill = bar.close * (1 + slippage * (1 if delta > 0 else -1))
        fee = abs(delta * fill) * fee_rate
        realized = 0.0
        if position and delta * position < 0:
            closing_qty = min(abs(position), abs(delta))
            realized = closing_qty * (fill - entry) * (1 if position > 0 else -1)
            if abs(delta) >= abs(position):
                entry = fill
        elif not position or delta * position > 0:
            entry = fill
        equity += realized - fee
        position += delta
        if abs(position) < 1e-12:
            position = 0.0
        trades.append(Trade(bar.timestamp, "buy" if delta > 0 else "sell", fill,
                            abs(delta), fee, realized, equity))
        peak = max(peak, equity)
        max_drawdown = max(max_drawdown, (peak - equity) / peak)
    unrealized = position * (bars[-1].close - entry) if bars and position else 0.0
    final_equity = equity + unrealized
    report = {
        "initial_equity": initial_equity,
        "final_equity": round(final_equity, 6),
        "net_return_pct": round((final_equity / initial_equity - 1) * 100, 6),
        "closed_realized_pnl": round(sum(t.realized_pnl for t in trades), 6),
        "fees_paid": round(sum(t.fee for t in trades), 6),
        "trade_events": len(trades),
        "max_drawdown_pct": round(max_drawdown * 100, 6),
        "open_position_quantity": round(position, 8),
        "data_source": "synthetic deterministic simulator; not dreamDEX testnet data",
    }
    return trades, report


def save_artifacts(trades: list[Trade], report: dict, out: str | Path) -> None:
    path = Path(out)
    path.mkdir(parents=True, exist_ok=True)
    with (path / "trades.jsonl").open("w", encoding="utf-8") as f:
        for trade in trades:
            f.write(json.dumps(asdict(trade), sort_keys=True) + "\n")
    (path / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
