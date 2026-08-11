"""
Core Domain Data Models.
All structures are strongly typed, immutable dataclasses representing state transitions.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID, uuid4

from app.domain.enums import (
    MarketRegime,
    SignalDirection,
    RiskDecision,
    RiskRejectionReason,
    ApprovalStatus,
    OrderExecutionState,
    ExitReason,
)


@dataclass(frozen=True)
class FeatureSnapshot:
    timestamp: datetime
    symbol: str
    timeframe: str
    features: Dict[str, float]
    feature_version: str


@dataclass(frozen=True)
class RegimeResult:
    regime: MarketRegime
    confidence: float
    timestamp: datetime
    model_version: str
    feature_version: str


@dataclass(frozen=True)
class Signal:
    signal_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    symbol: str = ""
    timeframe: str = ""
    direction: SignalDirection = SignalDirection.BUY
    entry_price: float = 0.0
    stop_loss: float = 0.0
    take_profit: float = 0.0
    strategy_name: str = ""
    strategy_version: str = ""
    signal_confidence: float = 0.0
    expiration: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class RiskAssessment:
    decision: RiskDecision
    max_allowed_volume: float
    reason: RiskRejectionReason
    calculated_risk_amount: float
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class TradeProposal:
    correlation_id: UUID
    signal: Signal
    regime_result: RegimeResult
    risk_assessment: RiskAssessment
    proposed_volume: float
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class ApprovalDecision:
    correlation_id: UUID
    discord_user_id: str
    status: ApprovalStatus
    decided_at: datetime
    modified_entry: Optional[float] = None
    modified_sl: Optional[float] = None
    modified_tp: Optional[float] = None


@dataclass(frozen=True)
class OrderRequest:
    idempotency_key: str
    correlation_id: UUID
    symbol: str
    direction: SignalDirection
    volume: float
    price: float
    stop_loss: float
    take_profit: float
    slippage_tolerance: int
    magic_number: int


@dataclass(frozen=True)
class OrderResult:
    idempotency_key: str
    correlation_id: UUID
    mt5_ticket: Optional[int]
    execution_state: OrderExecutionState
    fill_price: float
    filled_volume: float
    executed_at: datetime
    error_message: Optional[str] = None


@dataclass(frozen=True)
class Position:
    position_id: int
    correlation_id: UUID
    symbol: str
    direction: SignalDirection
    volume: float
    open_price: float
    stop_loss: float
    take_profit: float
    opened_at: datetime
    magic_number: int


@dataclass(frozen=True)
class TradeOutcome:
    correlation_id: UUID
    position_id: int
    symbol: str
    strategy_name: str
    regime: MarketRegime
    direction: SignalDirection
    entry_price: float
    exit_price: float
    realized_pnl: float
    r_multiple: float
    holding_seconds: float
    exit_reason: ExitReason
    closed_at: datetime


@dataclass(frozen=True)
class StrategyWeight:
    strategy_name: str
    regime: MarketRegime
    weight: float
    sample_size: int
    version_id: str
    updated_at: datetime


@dataclass(frozen=True)
class AccountState:
    balance: float
    equity: float
    margin: float
    free_margin: float
    daily_start_equity: float
    current_daily_drawdown_pct: float
    open_positions_count: int