"""
Verifiable Tests for the MT5 Adapter State Machine and Data Mapping.
These tests require the optional MetaTrader5 package and are skipped on
runners where MT5 is unavailable (for example Linux CI).
"""

import pytest
from unittest.mock import patch
from uuid import uuid4

mt5 = pytest.importorskip("MetaTrader5")

from app.data.mt5_adapter import MT5Adapter
from app.domain.enums import ConnectionState, SignalDirection, OrderExecutionState
from app.domain.models import OrderRequest


@pytest.fixture
def adapter():
    return MT5Adapter(login=12345, password="password", server="Test-Server")


@patch("app.data.mt5_adapter.MT5Client")
def test_connection_state_machine(mock_client, adapter):
    mock_client.initialize.return_value = True
    mock_client.terminal_info.return_value = {"connected": True}

    assert adapter.connect() is True
    assert adapter._state == ConnectionState.CONNECTED

    mock_client.terminal_info.return_value = {"connected": False}
    assert adapter.is_connected() is False
    assert adapter._state == ConnectionState.DEGRADED

    adapter.disconnect()
    assert adapter._state == ConnectionState.DISCONNECTED


@patch("app.data.mt5_adapter.MT5Client")
def test_send_order_success(mock_client, adapter):
    adapter._state = ConnectionState.CONNECTED
    mock_client.terminal_info.return_value = {"connected": True}
    mock_client.order_send.return_value = {
        "retcode": mt5.TRADE_RETCODE_DONE,
        "order": 987654321,
        "price": 1.0850,
        "volume": 0.1,
    }

    req = OrderRequest(
        idempotency_key="test_key_123",
        correlation_id=uuid4(),
        symbol="EURUSD",
        direction=SignalDirection.BUY,
        volume=0.1,
        price=1.0850,
        stop_loss=1.0800,
        take_profit=1.0900,
        slippage_tolerance=10,
        magic_number=555,
    )

    result = adapter.send_order(req)

    assert result.execution_state == OrderExecutionState.FILLED
    assert result.mt5_ticket == 987654321
    assert result.fill_price == 1.0850


@patch("app.data.mt5_adapter.MT5Client")
def test_send_order_ambiguous_failure(mock_client, adapter):
    adapter._state = ConnectionState.CONNECTED
    mock_client.terminal_info.return_value = {"connected": True}
    mock_client.order_send.return_value = None

    req = OrderRequest(
        idempotency_key="test_key_456",
        correlation_id=uuid4(),
        symbol="EURUSD",
        direction=SignalDirection.SELL,
        volume=0.1,
        price=1.0850,
        stop_loss=1.0900,
        take_profit=1.0800,
        slippage_tolerance=10,
        magic_number=555,
    )

    result = adapter.send_order(req)

    assert result.execution_state == OrderExecutionState.EXECUTION_UNCERTAIN
    assert adapter._state == ConnectionState.DEGRADED
    assert "Null response" in result.error_message
