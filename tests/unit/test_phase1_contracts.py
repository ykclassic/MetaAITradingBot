"""
Verifiable Tests for Phase 1 Domain Models, Enums, and Configuration Schema.
Ensures immutability, default assignments, and typing compliance.
"""

from datetime import datetime, timedelta
from uuid import uuid4
import pytest

from app.domain.enums import (
    MarketRegime,
    SignalDirection,
    RiskDecision,
    RiskRejectionReason,
    ApprovalStatus,
    OrderExecutionState,
)
from app.domain.models import (
    Signal,
    RiskAssessment,
    TradeProposal,
    RegimeResult,
    AccountState,
)
from app.config.schema import SystemConfig, RiskConfig


def test_signal_immutability():
    sig = Signal(
        symbol="EURUSD",
        timeframe="M15",
        direction=SignalDirection.BUY,
        entry_price=1.0850,
        stop_loss=1.0820,
        take_profit=1.0910,
        strategy_name="EMA_Trend",
        strategy_version="1.0.0",
        signal_confidence=0.85,
    )
    assert sig.symbol == "EURUSD"
    with pytest.raises(AttributeError):
        sig.symbol = "GBPUSD"  # Immutability check


def test_trade_proposal_construction():
    cid = uuid4()
    sig = Signal(symbol="EURUSD", direction=SignalDirection.BUY)
    regime = RegimeResult(
        regime=MarketRegime.STRONG_TREND_UP,
        confidence=0.92,
        timestamp=datetime.utcnow(),
        model_version="hmm_v1",
        feature_version="feat_v1",
    )
    risk = RiskAssessment(
        decision=RiskDecision.APPROVED,
        max_allowed_volume=0.1,
        reason=RiskRejectionReason.NONE,
        calculated_risk_amount=100.0,
    )
    
    proposal = TradeProposal(
        correlation_id=cid,
        signal=sig,
        regime_result=regime,
        risk_assessment=risk,
        proposed_volume=0.1,
        expires_at=datetime.utcnow() + timedelta(minutes=5),
    )
    
    assert proposal.correlation_id == cid
    assert proposal.risk_assessment.decision == RiskDecision.APPROVED


def test_default_config_schema():
    config = SystemConfig()
    assert config.dry_run is True
    assert config.risk.max_daily_drawdown_pct == 3.0
    assert config.risk.risk_per_trade_pct == 1.0