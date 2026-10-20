from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskConfig:
    risk_fraction: float = 0.01
    max_notional_fraction: float = 0.25
    max_leverage: float = 1.0
    stop_fraction: float = 0.02

    def validate(self) -> None:
        if not 0 < self.risk_fraction <= 0.02:
            raise ValueError("risk_fraction must be in (0, 0.02]")
        if not 0 < self.max_notional_fraction <= 1:
            raise ValueError("max_notional_fraction must be in (0, 1]")
        if not 0 < self.max_leverage <= 1:
            raise ValueError("simulator caps leverage at 1x")
        if not 0 < self.stop_fraction <= 0.1:
            raise ValueError("stop_fraction must be in (0, 0.1]")


def position_notional(equity: float, price: float, config: RiskConfig) -> float:
    config.validate()
    if equity <= 0 or price <= 0:
        return 0.0
    risk_based = equity * config.risk_fraction / config.stop_fraction
    cap = equity * config.max_notional_fraction * config.max_leverage
    return min(risk_based, cap)
