"""
System Configuration Dataclasses / Schemas.
Loaded from TOML and Environment variables with strict typing.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class RiskConfig:
    risk_per_trade_pct: float = 1.0
    max_daily_drawdown_pct: float = 3.0
    max_open_trades: int = 5
    max_spread_pips: float = 3.0
    max_slippage_pips: int = 10


@dataclass(frozen=True)
class SystemConfig:
    environment: str = "development"
    dry_run: bool = True
    symbols: List[str] = field(default_factory=lambda: ["EURUSD", "GBPUSD"])
    timeframes: List[str] = field(default_factory=lambda: ["M15", "H1"])
    risk: RiskConfig = field(default_factory=RiskConfig)