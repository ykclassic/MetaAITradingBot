"""
Verifiable Tests for the Risk Management Layer.
Ensures drawdown limits are respected and position sizing math is perfectly accurate.
"""

import pytest
from datetime import datetime, timedelta, timezone

from app.risk.manager import StandardRiskManager
from app.domain.models import Signal, AccountState
from app.domain.enums import SignalDirection


@pytest.fixture
def base_account():
    return AccountState(
        balance=10000.0,
        equity=10000.0,
        margin=0.0,
        free_margin=10000.0,
        daily_start_equity=10000.0,
        current_daily_drawdown_pct=0.01, # 1% drawdown currently
        open_positions_count=1
    )

@pytest.fixture
def buy_signal():
    return Signal(
        symbol="EURUSD",
        timeframe="M15",
        direction=SignalDirection.BUY,
        entry_price=1.1000,
        stop_loss=1.0950, # 50 pips (0.0050) SL
        take_profit=1.1100,
        strategy_name="EMA_Trend",
        strategy_version="1.0",
        signal_confidence=0.85,
        expiration=datetime.now(timezone.utc) + timedelta(minutes=15)
    )

def test_risk_manager_calculates_correct_volume(base_account, buy_signal):
    manager = StandardRiskManager(
        risk_per_trade_pct=0.01, # Risking 1% of 10,000 = $100
        contract_size=100000.0
    )
    
    order = manager.evaluate_signal(buy_signal, base_account)
    
    assert order is not None
    # Math Verification:
    # Risk Amount = 10000 * 0.01 = $100
    # SL Distance = 1.1000 - 1.0950 = 0.0050
    # Raw Volume = 100 / (0.0050 * 100000) = 100 / 500 = 0.20 lots
    assert order.volume == 0.20
    assert order.symbol == "EURUSD"
    assert order.direction == SignalDirection.BUY

def test_risk_manager_rejects_max_positions(base_account, buy_signal):
    base_account.open_positions_count = 3
    manager = StandardRiskManager(max_open_positions=3)
    
    order = manager.evaluate_signal(buy_signal, base_account)
    
    assert order is None

def test_risk_manager_rejects_max_drawdown(base_account, buy_signal):
    base_account.current_daily_drawdown_pct = 0.06 # 6% drawdown
    manager = StandardRiskManager(max_daily_drawdown_pct=0.05) # 5% limit
    
    order = manager.evaluate_signal(buy_signal, base_account)
    
    assert order is None

def test_risk_manager_rejects_micro_lot_breach(base_account, buy_signal):
    # Test a scenario where the stop loss is so wide, or equity so low, that risk < 0.01 lots
    base_account.equity = 100.0 # Only $100 equity
    buy_signal.stop_loss = 1.0000 # 1000 pips (0.1000) SL
    
    manager = StandardRiskManager(risk_per_trade_pct=0.01) # Risking $1
    
    # Math: 1 / (0.1000 * 100000) = 1 / 10000 = 0.0001 lots (Below 0.01 limit)
    order = manager.evaluate_signal(buy_signal, base_account)
    
    assert order is None