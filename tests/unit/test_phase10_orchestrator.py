"""
Verifiable Tests for the Pipeline Orchestrator.
Ensures correct data flow and graceful handling of component failures.
"""

import pytest
from unittest.mock import MagicMock

from app.pipeline.orchestrator import TradingPipeline
from app.domain.enums import OrderExecutionState
from app.domain.models import OrderResult


@pytest.fixture
def mock_dependencies():
    return {
        "adapter": MagicMock(),
        "feature_engine": MagicMock(),
        "regime_detector": MagicMock(),
        "strategies": [MagicMock(), MagicMock()],
        "signal_selector": MagicMock(),
        "risk_manager": MagicMock(),
        "execution_engine": MagicMock()
    }


def test_pipeline_successful_cycle(mock_dependencies):
    deps = mock_dependencies
    deps["adapter"].is_connected.return_value = True
    deps["adapter"].get_account_state.return_value = MagicMock()
    deps["adapter"].get_ohlcv.return_value = [{"close": 1.0}]
    deps["feature_engine"].compute_features.return_value = MagicMock()
    deps["regime_detector"].predict.return_value = MagicMock()

    mock_signal = MagicMock()
    deps["strategies"][0].generate_signal.return_value = mock_signal
    deps["strategies"][1].generate_signal.return_value = None
    deps["signal_selector"].select_best_signal.return_value = mock_signal
    deps["risk_manager"].evaluate_signal.return_value = MagicMock()

    success_result = MagicMock()
    success_result.execution_state = OrderExecutionState.FILLED
    deps["execution_engine"].execute_order.return_value = success_result

    pipeline = TradingPipeline(**deps, symbols=["EURUSD"], timeframe="M15", lookback_periods=100)
    pipeline.run_cycle()

    deps["adapter"].get_ohlcv.assert_called_once_with("EURUSD", "M15", 100)
    deps["feature_engine"].compute_features.assert_called_once()
    deps["signal_selector"].select_best_signal.assert_called_once_with([mock_signal])
    deps["execution_engine"].execute_order.assert_called_once()


def test_pipeline_halts_on_execution_uncertain(mock_dependencies):
    deps = mock_dependencies
    deps["adapter"].is_connected.return_value = True
    deps["adapter"].get_account_state.return_value = MagicMock()
    deps["adapter"].get_ohlcv.return_value = [{"close": 1.0}]
    deps["feature_engine"].compute_features.return_value = MagicMock()
    deps["regime_detector"].predict.return_value = MagicMock()
    deps["strategies"][0].generate_signal.return_value = MagicMock()
    deps["strategies"][1].generate_signal.return_value = None
    deps["signal_selector"].select_best_signal.return_value = MagicMock()
    deps["risk_manager"].evaluate_signal.return_value = MagicMock()

    uncertain_result = OrderResult(
        idempotency_key="123",
        correlation_id=MagicMock(),
        order_id=None,
        execution_state=OrderExecutionState.EXECUTION_UNCERTAIN,
        fill_price=0.0,
        filled_volume=0.0,
        executed_at=MagicMock(),
    )
    deps["execution_engine"].execute_order.return_value = uncertain_result

    pipeline = TradingPipeline(**deps, symbols=["EURUSD"])
    pipeline.is_running = True
    pipeline.run_cycle()

    assert pipeline.is_running is False


def test_pipeline_skips_symbol_on_feature_error(mock_dependencies):
    deps = mock_dependencies
    deps["adapter"].is_connected.return_value = True
    deps["adapter"].get_ohlcv.return_value = [{"close": 1.0}]
    deps["feature_engine"].compute_features.side_effect = ValueError("NaN detected")

    pipeline = TradingPipeline(**deps, symbols=["EURUSD", "GBPUSD"])
    pipeline.run_cycle()

    deps["execution_engine"].execute_order.assert_not_called()
    assert deps["adapter"].get_ohlcv.call_count == 2
