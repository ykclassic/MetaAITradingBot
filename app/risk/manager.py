"""
Risk Management Engine.
Enforces drawdown limits, max positions, and calculates position sizing deterministically.
"""

import logging
from typing import Optional
from uuid import uuid4

from app.core.interfaces import RiskManagerProtocol
from app.domain.models import Signal, AccountState, OrderRequest

logger = logging.getLogger(__name__)


class StandardRiskManager(RiskManagerProtocol):
    """Implements standard fixed-fractional risk management."""

    def __init__(
        self,
        risk_per_trade_pct: float = 0.01,
        max_daily_drawdown_pct: float = 0.05,
        max_open_positions: int = 3,
        contract_size: float = 100000.0,
    ):
        self.risk_per_trade_pct = risk_per_trade_pct
        self.max_daily_drawdown_pct = max_daily_drawdown_pct
        self.max_open_positions = max_open_positions
        self.contract_size = contract_size

    def evaluate_signal(self, signal: Signal, account_state: AccountState) -> Optional[OrderRequest]:
        """Return an order request when account constraints permit the trade."""
        if account_state.open_positions_count >= self.max_open_positions:
            logger.warning(
                f"Risk Manager rejected signal: Max open positions ({self.max_open_positions}) reached."
            )
            return None

        if account_state.current_daily_drawdown_pct >= self.max_daily_drawdown_pct:
            logger.warning(
                f"Risk Manager rejected signal: Max daily drawdown ({self.max_daily_drawdown_pct * 100}%) exceeded."
            )
            return None

        volume = self._calculate_position_size(
            equity=account_state.equity,
            entry_price=signal.entry_price,
            stop_loss=signal.stop_loss,
        )

        if volume < 0.01:
            logger.warning(
                f"Risk Manager rejected signal: Calculated volume ({volume}) is below minimum lot size (0.01)."
            )
            return None

        return OrderRequest(
            idempotency_key=str(uuid4()),
            correlation_id=uuid4(),
            symbol=signal.symbol,
            direction=signal.direction,
            volume=volume,
            price=signal.entry_price,
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
            slippage_tolerance=10,
            magic_number=self._generate_magic_number(signal.strategy_name),
        )

    def _calculate_position_size(self, equity: float, entry_price: float, stop_loss: float) -> float:
        """
        Calculates standard-lot volume from fixed fractional risk.
        Formula: (Equity * Risk_Pct) / (Stop_Loss_Distance * Contract_Size)
        """
        risk_amount = equity * self.risk_per_trade_pct
        sl_distance = abs(entry_price - stop_loss)
        if sl_distance <= 0:
            return 0.0

        raw_volume = risk_amount / (sl_distance * self.contract_size)
        # Round to the broker's 0.01 lot step using decimal-safe rounding.
        return round(raw_volume, 2)

    def _generate_magic_number(self, strategy_name: str) -> int:
        return abs(hash(strategy_name)) % (10**8)
