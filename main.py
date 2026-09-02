"""Application entry point."""

import logging
import os
import sys

from dotenv import load_dotenv

from app.allocation.selector import PrioritySignalSelector
from app.config import AppConfig
from app.data.xt_adapter import XTAdapter
from app.execution.engine import ExecutionEngine
from app.features.engine import PandasFeatureEngine
from app.monitor.discord import DiscordSystemMonitor
from app.persistence.database import SQLiteManager
from app.performance.tracker import PerformanceTracker
from app.pipeline.orchestrator import TradingPipeline
from app.regimes.hmm_detector import HMMRegimeDetector
from app.regimes.manager import ModelManager
from app.risk.manager import StandardRiskManager
from app.strategies.implementations import (
    ATRBreakoutStrategy,
    EMATrendStrategy,
    RSIMeanReversionStrategy,
)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def build_pipeline(config: AppConfig) -> TradingPipeline:
    adapter = XTAdapter(api_key=config.xt_api_key, secret_key=config.xt_secret_key)
    model_manager = ModelManager(model_dir=config.model_dir)
    monitor = DiscordSystemMonitor(config.discord_webhook_url)
    performance_tracker = PerformanceTracker(SQLiteManager(config.performance_db_path))

    model_path = os.path.join(config.model_dir, f"hmm_v_{config.model_version}.joblib")
    mapping_path = os.path.join(config.model_dir, f"mapping_v_{config.model_version}.json")
    model_missing = not (os.path.exists(model_path) and os.path.exists(mapping_path))

    if model_missing:
        if config.live_trading_enabled:
            raise FileNotFoundError(
                f"Model version {config.model_version} missing files. "
                "A prevalidated model artifact is required when live trading is enabled."
            )

        logger = logging.getLogger("main")
        logger.warning(
            "Model %s is missing; safe verification mode will bootstrap a temporary model "
            "from fresh XT.com candles. LIVE_TRADING_ENABLED remains false.",
            config.model_version,
        )
        if not adapter.connect():
            raise RuntimeError("Unable to connect to XT.com for verification model bootstrap")

        candles_by_symbol = {}
        bootstrap_count = max(config.lookback_periods, 200)
        for symbol in config.symbols:
            candles_by_symbol[symbol] = adapter.get_ohlcv(
                symbol,
                config.timeframe,
                bootstrap_count,
            )

        model_manager.bootstrap_from_candles(
            candles_by_symbol=candles_by_symbol,
            version_id=config.model_version,
            timeframe=config.timeframe,
        )

    regime_detector = HMMRegimeDetector(
        manager=model_manager,
        version_id=config.model_version,
        confidence_threshold=config.model_confidence_threshold,
    )

    return TradingPipeline(
        adapter=adapter,
        feature_engine=PandasFeatureEngine(),
        regime_detector=regime_detector,
        strategies=[EMATrendStrategy(), RSIMeanReversionStrategy(), ATRBreakoutStrategy()],
        signal_selector=PrioritySignalSelector(),
        risk_manager=StandardRiskManager(
            risk_per_trade_pct=config.risk_per_trade_pct,
            max_daily_drawdown_pct=config.max_daily_drawdown_pct,
            max_open_positions=config.max_open_positions,
            contract_size=config.contract_size,
        ),
        execution_engine=ExecutionEngine(
            adapter=adapter,
            live_trading_enabled=config.live_trading_enabled,
        ),
        symbols=config.symbols,
        timeframe=config.timeframe,
        lookback_periods=config.lookback_periods,
        monitor=monitor,
        performance_tracker=performance_tracker,
    )


def main() -> None:
    setup_logging()
    logger = logging.getLogger("main")
    load_dotenv()
    config = AppConfig.load_from_env()

    run_once = os.environ.get("RUN_ONCE", "true").lower() in {"1", "true", "yes"}
    pipeline = build_pipeline(config)
    try:
        if run_once:
            if not pipeline.adapter.is_connected() and not pipeline.adapter.connect():
                raise RuntimeError("Unable to connect to XT.com")
            pipeline.run_cycle()
        else:
            pipeline.start(cycle_interval_seconds=config.cycle_interval_seconds)
    except KeyboardInterrupt:
        logger.info("Manual shutdown requested.")
    finally:
        pipeline.stop()


if __name__ == "__main__":
    main()
