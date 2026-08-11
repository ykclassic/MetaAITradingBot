"""
Verifiable Tests for the Execution Engine.
Ensures idempotency, correct adapter routing, and exception safety.
"""

import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime, timezone

from app.execution.engine import ExecutionEngine
from app.domain.models import OrderRequest, OrderResult
from app.domain.enums import SignalDirection, OrderExecutionState


@pytest.fixture
def mock_adapter():
    return MagicMock()

@pytest.fixture
def base_request():
    return OrderRequest(
        idempotency_key=str(uuid4()),
        correlation_id=uuid4(),
        symbol="EURUSD",
        direction=SignalDirection.BUY,
        volume=0.1,
        price=1.1000,
        stop_loss=1.0950,
        take_profit=1.1100,
        slippage_tolerance=10,
        magic_number=12345
    )

def test_execution_engine_success(mock_adapter, base_request):
    # Arrange
    success_result = OrderResult(
        idempotency_key=base_request.idempotency_key,
        correlation_id=base_request.correlation_id,
        mt5_ticket=999999,
        execution_state=OrderExecutionState.FILLED,
        fill_price=1.1000,
        filled_volume=0.1,
        executed_at=datetime.now(timezone.utc)
    )
    mock_adapter.send_order.return_value = success_result
    engine = ExecutionEngine(adapter=mock_adapter)

    # Act
    result = engine.execute_order(base_request)

    # Assert
    assert result.execution_state == OrderExecutionState.FILLED
    assert result.mt5_ticket == 999999
    mock_adapter.send_order.assert_called_once_with(base_request)
    assert base_request.idempotency_key in engine._processed_requests


def test_execution_engine_idempotency_blocks_duplicates(mock_adapter, base_request):
    # Arrange
    engine = ExecutionEngine(adapter=mock_adapter)
    
    # Act - First Call
    engine.execute_order(base_request)
    
    # Act - Second Call with same request/key
    result = engine.execute_order(base_request)

    # Assert
    assert result.execution_state == OrderExecutionState.REJECTED_BY_BROKER
    assert "Idempotency key already processed" in result.error_message
    # Adapter should only be called once despite two execute_order calls
    mock_adapter.send_order.assert_called_once()


def test_execution_engine_catches_unhandled_adapter_exceptions(mock_adapter, base_request):
    # Arrange
    # Simulate a catastrophic failure in the adapter (e.g., C-binding crash wrapped as Exception)
    mock_adapter.send_order.side_effect = RuntimeError("MT5 Terminal unresponsive")
    engine = ExecutionEngine(adapter=mock_adapter)

    # Act
    result = engine.execute_order(base_request)

    # Assert
    assert result.execution_state == OrderExecutionState.EXECUTION_UNCERTAIN
    assert "Unhandled exception" in result.error_message
    assert "MT5 Terminal unresponsive" in result.error_message