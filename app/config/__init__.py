"""Runtime environment configuration package."""

import os
import unicodedata
from dataclasses import dataclass
from typing import List

from .schema import RiskConfig, SystemConfig


DEFAULT_TRADE_SYMBOLS = "BTC_USDT,ETH_USDT,SOL_USDT,BNB_USDT,XRP_USDT,ADA_USDT,LINK_USDT"


def _clean_secret(name: str) -> str:
    """Normalize credentials copied through shells/UI and remove hidden Unicode marks."""
    value = unicodedata.normalize("NFKC", os.getenv(name, "")).strip()
    value = "".join(ch for ch in value if unicodedata.category(ch) not in {"Cf", "Cc"})
    if value and any(ord(ch) > 255 for ch in value):
        raise ValueError(f"{name} contains unsupported non-HTTP-header characters")
    return value


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
    live_trading_enabled: bool = False
    xt_api_key: str = ""
    xt_secret_key: str = ""
    discord_webhook_url: str = ""
    performance_db_path: str = "data/trading_system.sqlite"

    @classmethod
    def load_from_env(cls) -> "AppConfig":
        symbols = [
            s.strip().upper()
            for s in os.getenv("TRADE_SYMBOLS", DEFAULT_TRADE_SYMBOLS).split(",")
            if s.strip()
        ]
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
            live_trading_enabled=os.getenv("LIVE_TRADING_ENABLED", "false").lower() in {"1", "true", "yes"},
            xt_api_key=_clean_secret("XT_API_KEY"),
            xt_secret_key=_clean_secret("XT_SECRET_KEY"),
            discord_webhook_url=os.getenv("DISCORD_WEBHOOK_URL", "").strip(),
            performance_db_path=os.getenv("PERFORMANCE_DB_PATH", "data/trading_system.sqlite"),
        )


__all__ = ["AppConfig", "RiskConfig", "SystemConfig", "DEFAULT_TRADE_SYMBOLS"]
