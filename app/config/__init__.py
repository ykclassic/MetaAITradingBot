"""Runtime environment configuration package."""

import os
from dataclasses import dataclass
from typing import List

from .schema import RiskConfig, SystemConfig


@dataclass(frozen=True)
class AppConfig:
    symbols: List[str]
    timeframe: str
    risk_per_trade_pct: float
    max_daily_drawdown_pct: float
    max_open_positions: int
    model_version: str
    model_dir: str
    model_confidence_threshold: float
    cycle_interval_seconds: int
    lookback_periods: int
    contract_size: float
    xt_api_key: str = ""
    xt_secret_key: str = ""

    @classmethod
    def load_from_env(cls) -> "AppConfig":
        symbols = [s.strip() for s in os.getenv("TRADE_SYMBOLS", "BTC_USDT,ETH_USDT").split(",") if s.strip()]
        return cls(
            symbols=symbols,
            timeframe=os.getenv("TIMEFRAME", "M15"),
            risk_per_trade_pct=float(os.getenv("RISK_PER_TRADE_PCT", "0.01")),
            max_daily_drawdown_pct=float(os.getenv("MAX_DAILY_DRAWDOWN_PCT", "0.05")),
            max_open_positions=int(os.getenv("MAX_OPEN_POSITIONS", "3")),
            model_version=os.getenv("MODEL_VERSION", "v1.0.0"),
            model_dir=os.getenv("MODEL_DIR", "models/"),
            model_confidence_threshold=float(os.getenv("MODEL_CONFIDENCE_THRESHOLD", "0.65")),
            cycle_interval_seconds=int(os.getenv("CYCLE_INTERVAL_SECONDS", "60")),
            lookback_periods=int(os.getenv("LOOKBACK_PERIODS", "100")),
            contract_size=float(os.getenv("CONTRACT_SIZE", "1.0")),
            xt_api_key=os.getenv("XT_API_KEY", ""),
            xt_secret_key=os.getenv("XT_SECRET_KEY", ""),
        )


__all__ = ["AppConfig", "RiskConfig", "SystemConfig"]
