from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Bar:
    timestamp: int
    close: float


def sma(values: list[float], period: int) -> float | None:
    if period <= 0 or len(values) < period:
        return None
    return sum(values[-period:]) / period


def rsi(values: list[float], period: int = 14) -> float | None:
    if period <= 0 or len(values) <= period:
        return None
    changes = [b - a for a, b in zip(values[-period-1:], values[-period:])]
    gains = sum(max(x, 0.0) for x in changes) / period
    losses = sum(max(-x, 0.0) for x in changes) / period
    if losses == 0:
        return 100.0 if gains else 50.0
    return 100 - 100 / (1 + gains / losses)


def crossover_signal(history: Iterable[Bar], fast: int = 8, slow: int = 21) -> int:
    """Return target direction: +1 long, -1 short, 0 no signal."""
    closes = [bar.close for bar in history]
    f, s = sma(closes, fast), sma(closes, slow)
    momentum = rsi(closes, 14)
    if f is None or s is None or momentum is None:
        return 0
    if f > s and momentum < 70:
        return 1
    if f < s and momentum > 30:
        return -1
    return 0
