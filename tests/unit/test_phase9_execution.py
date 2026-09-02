"""Execution engine tests for broker routing, idempotency, and safety."""

from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.domain.enums import OrderExecutionState, SignalDirection
from app.domain.models import OrderRequest, OrderResult
from app.execution.engine import ExecutionEngine


@pytest.fixture
def mock_adapter():
    return MagicMock()


@pytest.fixture
def base_request():
    return OrderRequest(
        idempotency_key=str(uuid4()),
        correlation_id=uuid4(),
        symbol="BTC_USDT",
        direction=SignalDirection.BUY,
        volume=0.01,
        price=100000.0,
        stop_loss=99000.0,
        take_profit=102000.0,
        slippage_tolerance=10,
        magic_number=12345,
    )


def test_execution_engine_success(mock_adapter, base_request):
    success_result = OrderResult(
        idempotency_key=base_request.idempotency_key,
        correlation_id=base_request.correlation_id,
        order_id=999999,
        execution_state=OrderExecutionState.IN_FLIGHT,
        fill_price=0.0,
        filled_volume=0.0,
        executed_at=datetime.now(timezone.utc),
    )
    mock_adapter.send_order.return_value = success_result

    engine = ExecutionEngine(adapter=mock_adapter, live_trading_enabled=True)
    result = engine.execute_order(base_request)

    assert result.execution_state == OrderExecutionState.IN_FLIGHT
    assert result.order_id == 999999
    mock_adapter.send_order.assert_called_once_with(base_request)
    assert base_request.idempotency_key in engine._processed_requests


def test_execution_engine_blocks_order_when_live_trading_disabled(mock_adapter, base_request):
    engine = ExecutionEngine(adapter=mock_adapter, live_trading_enabled=False)

    result = engine.execute_order(base_request)

    assert result.execution_state == OrderExecutionState.CANCELLED
    assert "Live trading disabled" in result.error_message
    mock_adapter.send_order.assert_not_called()


def test_execution_engine_idempotency_blocks_duplicates(mock_adapter, base_request):
    mock_adapter.send_order.return_value = OrderResult(
        idempotency_key=base_request.idempotency_key,
        correlation_id=base_request.correlation_id,
        order_id=123,
        execution_state=OrderExecutionState.IN_FLIGHT,
        fill_price=0.0,
        filled_volume=0.0,
        executed_at=datetime.now(timezone.utc),
    )
    engine = ExecutionEngine(adapter=mock_adapter, live_trading_enabled=True)

    engine.execute_order(base_request)
    result = engine.execute_order(base_request)

    assert result.execution_state == OrderExecutionState.REJECTED_BY_BROKER
    assert "Idempotency key already processed" in result.error_message
    mock_adapter.send_order.assert_called_once()


def test_execution_engine_catches_adapter_exceptions(mock_adapter, base_request):
    mock_adapter.send_order.side_effect = RuntimeError("XT transport failure")
    engine = ExecutionEngine(adapter=mock_adapter, live_trading_enabled=True)

    result = engine.execute_order(base_request)

    assert result.execution_state == OrderExecutionState.EXECUTION_UNCERTAIN
    assert "Unhandled exception" in result.error_message
    assert "XT transport failure" in result.error_message
