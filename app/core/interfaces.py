"""
Core System Protocol Interfaces.
Enforces Dependency Inversion across all major sub-systems.
"""

from typing import Protocol, List, Optional
from uuid import UUID

from app.domain.models import (
    FeatureSnapshot,
    RegimeResult,
    Signal,
    RiskAssessment,
    TradeProposal,
    ApprovalDecision,
    OrderRequest,
    OrderResult,
    Position,
    TradeOutcome,
    AccountState,
)


class MarketDataAdapter(Protocol):
    def connect(self) -> bool: ...
    def disconnect(self) -> None: ...
    def is_connected(self) -> bool: ...
    def get_account_state(self) -> AccountState: ...
    def get_ohlcv(self, symbol: str, timeframe: str, count: int) -> List[dict]: ...
    def send_order(self, request: OrderRequest) -> OrderResult: ...
    def get_open_positions(self) -> List[Position]: ...


class FeatureEngineProtocol(Protocol):
    def compute_features(self, symbol: str, timeframe: str, candles: List[dict]) -> FeatureSnapshot: ...


class RegimeDetectorProtocol(Protocol):
    def predict(self, features: FeatureSnapshot) -> RegimeResult: ...


class StrategyProtocol(Protocol):
    name: str
    version: str
    def generate_signal(self, features: FeatureSnapshot, regime: RegimeResult) -> Optional[Signal]: ...


class RiskManagerProtocol(Protocol):
    def evaluate(self, signal: Signal, account_state: AccountState, current_spread: float) -> RiskAssessment: ...


class ApprovalGatewayProtocol(Protocol):
    async def request_approval(self, proposal: TradeProposal) -> ApprovalDecision: ...


class ExecutionEngineProtocol(Protocol):
    def execute_proposal(self, proposal: TradeProposal, decision: ApprovalDecision) -> OrderResult: ...


class TradeRepositoryProtocol(Protocol):
    def save_signal(self, signal: Signal) -> None: ...
    def save_trade_outcome(self, outcome: TradeOutcome) -> None: ...
    def get_trade_outcomes(self, strategy_name: str, regime: str) -> List[TradeOutcome]: ...