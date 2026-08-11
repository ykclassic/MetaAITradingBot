"""
Application Entry Point (Composition Root).
Wires dependencies, configures logging, and starts the system.
"""

import logging
import sys
from dotenv import load_dotenv

from app.config import AppConfig
from app.data.mt5_adapter import MT5Adapter
from app.features.engine import PandasFeatureEngine
from app.regimes.manager import ModelManager
from app.regimes.hmm_detector import HMMRegimeDetector
from app.strategies.implementations import EMATrendStrategy, RSIMeanReversionStrategy, ATRBreakoutStrategy
from app.allocation.selector import PrioritySignalSelector
from app.risk.manager import StandardRiskManager
from app.execution.engine import ExecutionEngine
from app.pipeline.orchestrator import TradingPipeline

def setup_logging():
    """Configures centralized, structured logging to standard output."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    # Silence verbose external libraries
    logging.getLogger("hmmlearn").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

def main():
    # 1. Initialize Logging & Config
    setup_logging()
    logger = logging.getLogger("main")
    logger.info("Bootstrapping Algorithmic Trading System...")
    
    # Load .env file if running locally
    load_dotenv()
    config = AppConfig.load_from_env()

    # 2. Instantiate Data & Feature Layers
    adapter = MT5Adapter(
        login=config.mt5_login,
        password=config.mt5_password,
        server=config.mt5_server,
        path=config.mt5_path
    )
    
    feature_engine = PandasFeatureEngine()

    # 3. Instantiate Machine Learning Regime Layer
    model_manager = ModelManager(model_dir="models/")
    regime_detector = HMMRegimeDetector(
        manager=model_manager,
        version_id=config.model_version,
        confidence_threshold=0.65
    )

    # 4. Instantiate Strategy Portfolio
    strategies = [
        EMATrendStrategy(),
        RSIMeanReversionStrategy(),
        ATRBreakoutStrategy()
    ]

    # 5. Instantiate Arbitration & Risk Layers
    signal_selector = PrioritySignalSelector()
    
    risk_manager = StandardRiskManager(
        risk_per_trade_pct=config.risk_per_trade_pct,
        max_daily_drawdown_pct=config.max_daily_drawdown_pct,
        max_open_positions=config.max_open_positions,
        contract_size=100000.0  # Standard forex lot
    )

    # 6. Instantiate Execution Layer
    execution_engine = ExecutionEngine(adapter=adapter)

    # 7. Wire the Orchestrator
    pipeline = TradingPipeline(
        adapter=adapter,
        feature_engine=feature_engine,
        regime_detector=regime_detector,
        strategies=strategies,
        signal_selector=signal_selector,
        risk_manager=risk_manager,
        execution_engine=execution_engine,
        symbols=config.symbols,
        timeframe=config.timeframe,
        lookback_periods=100
    )

    # 8. Launch the continuous loop
    try:
        pipeline.start(cycle_interval_seconds=60)
    except KeyboardInterrupt:
        logger.info("Manual shutdown requested.")
    finally:
        logger.info("System has been gracefully terminated.")

if __name__ == "__main__":
    main()