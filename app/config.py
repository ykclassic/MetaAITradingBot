"""
Environment-based Configuration Manager.
Loads and validates critical settings from the environment.
"""

import os
import logging
from dataclasses import dataclass
from typing import List

logger = logging.getLogger(__name__)

@dataclass
class AppConfig:
    # Broker Credentials
    mt5_login: int
    mt5_password: str
    mt5_server: str
    mt5_path: str = ""
    
    # Trading Parameters
    symbols: List[str]
    timeframe: str
    risk_per_trade_pct: float
    max_daily_drawdown_pct: float
    max_open_positions: int
    
    # Model Configuration
    model_version: str

    @classmethod
    def load_from_env(cls) -> "AppConfig":
        """Safely loads configuration from environment variables."""
        try:
            return cls(
                mt5_login=int(os.environ["MT5_LOGIN"]),
                mt5_password=os.environ["MT5_PASSWORD"],
                mt5_server=os.environ["MT5_SERVER"],
                mt5_path=os.environ.get("MT5_PATH", ""),
                
                # Defaulting to EURUSD and GBPUSD if not specified
                symbols=os.environ.get("TRADE_SYMBOLS", "EURUSD,GBPUSD").split(","),
                timeframe=os.environ.get("TIMEFRAME", "M15"),
                
                risk_per_trade_pct=float(os.environ.get("RISK_PER_TRADE_PCT", "0.01")),
                max_daily_drawdown_pct=float(os.environ.get("MAX_DAILY_DRAWDOWN_PCT", "0.05")),
                max_open_positions=int(os.environ.get("MAX_OPEN_POSITIONS", "3")),
                
                model_version=os.environ.get("MODEL_VERSION", "v1")
            )
        except KeyError as e:
            logger.critical(f"Missing required environment variable: {e}")
            raise SystemExit(f"Configuration Error: Missing {e}")
        except ValueError as e:
            logger.critical(f"Invalid environment variable type: {e}")
            raise SystemExit(f"Configuration Error: {e}")