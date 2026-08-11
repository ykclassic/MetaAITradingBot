"""
Verifiable Tests for Database Persistence and Domain Mapping.
Uses an in-memory SQLite database to avoid disk I/O side effects during testing.
"""

import pytest
from uuid import uuid4
from datetime import datetime

from app.persistence.database import SQLiteManager
from app.persistence.repositories import SQLiteTradeRepository
from app.domain.models import Signal, TradeOutcome
from app.domain.enums import SignalDirection, MarketRegime, ExitReason


@pytest.fixture
def db_manager():
    # Use in-memory database for clean, isolated integration tests
    manager = SQLiteManager(db_path=":memory:")
    return manager


@pytest.fixture
def repository(db_manager):
    return SQLiteTradeRepository(db_manager)


def test_save_and_retrieve_trade_outcome(repository):
    # 1. Arrange: Create a valid TradeOutcome domain model
    correlation_id = uuid4()
    outcome = TradeOutcome(
        correlation_id=correlation_id,
        position_id=123456,
        symbol="EURUSD",
        strategy_name="EMA_Trend",
        regime=MarketRegime.STRONG_TREND_UP,
        direction=SignalDirection.BUY,
        entry_price=1.0800,
        exit_price=1.0850,
        realized_pnl=50.0,
        r_multiple=2.5,
        holding_seconds=3600.0,
        exit_reason=ExitReason.TAKE_PROFIT,
        closed_at=datetime.utcnow()
    )

    # 2. Act: Save to repository
    repository.save_trade_outcome(outcome)

    # 3. Assert: Retrieve and verify data mappings (Enum resolution, UUID parsing)
    results = repository.get_trade_outcomes("EMA_Trend", MarketRegime.STRONG_TREND_UP.value)
    
    assert len(results) == 1
    retrieved = results[0]
    
    assert retrieved.correlation_id == correlation_id
    assert retrieved.symbol == "EURUSD"
    assert retrieved.regime == MarketRegime.STRONG_TREND_UP
    assert retrieved.exit_reason == ExitReason.TAKE_PROFIT
    assert retrieved.r_multiple == 2.5


def test_save_signal(repository, db_manager):
    # 1. Arrange
    sig = Signal(
        symbol="GBPUSD",
        direction=SignalDirection.SELL,
        entry_price=1.2500,
        stop_loss=1.2550,
        take_profit=1.2400,
        strategy_name="ATR_Breakout",
        strategy_version="1.0"
    )

    # 2. Act
    repository.save_signal(sig)

    # 3. Assert: Verify raw insertion directly via DB to ensure schema compliance
    with db_manager.get_connection() as conn:
        cursor = conn.execute("SELECT * FROM signals WHERE symbol = 'GBPUSD'")
        row = cursor.fetchone()
        
        assert row is not None
        assert row["direction"] == "SELL"
        assert row["strategy_name"] == "ATR_Breakout"