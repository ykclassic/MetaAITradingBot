"""
Risk Management Engine.
Enforces drawdown limits, max positions, and calculates position sizing deterministically.
"""

import logging
from typing import Optional
from uuid import uuid4

from app.core.interfaces import RiskManagerProtocol
from app.domain.models import Signal, AccountState, OrderRequest
from app.domain.enums import SignalDirection

logger = logging.getLogger(__name__)


class StandardRiskManager(RiskManagerProtocol):
    """
    Implements standard fixed-fractional risk management.
    """
    
    def __init__(self, 
                 risk_per_trade_pct: float = 0.01, 
                 max_daily_drawdown_pct: float = 0.05, 
                 max_open_positions: int = 3,
                 contract_size: float = 100000.0):
        self.risk_per_trade_pct = risk_per_trade_pct
        self.max_daily_drawdown_pct = max_daily_drawdown_pct
        self.max_open_positions = max_open_positions
        self.contract_size = contract_size

    def evaluate_signal(self, signal: Signal, account_state: AccountState) -> Optional[OrderRequest]:
        """
        Evaluates a signal against account constraints and calculates position size.
        Returns an OrderRequest if safe, or None if the trade is rejected.
        """
        # 1. Verify Global Constraints
        if account_state.open_positions_count >= self.max_open_positions:
            logger.warning(f"Risk Manager rejected signal: Max open positions ({self.max_open_positions}) reached.")
            return None
            
        if account_state.current_daily_drawdown_pct >= self.max_daily_drawdown_pct:
            logger.warning(f"Risk Manager rejected signal: Max daily drawdown ({self.max_daily_drawdown_pct * 100}%) exceeded.")
            return None

        # 2. Calculate Position Size (Volume)
        volume = self._calculate_position_size(
            equity=account_state.equity,
            entry_price=signal.entry_price,
            stop_loss=signal.stop_loss
        )
        
        # Ensure volume is valid (e.g., >= 0.01 micro lots for MT5)
        if volume < 0.01:
            logger.warning(f"Risk Manager rejected signal: Calculated volume ({volume}) is below minimum lot size (0.01).")
            return None

        # 3. Construct the verified OrderRequest
        return OrderRequest(
            idempotency_key=str(uuid4()),
            correlation_id=uuid4(),
            symbol=signal.symbol,
            direction=signal.direction,
            volume=volume,
            price=signal.entry_price,
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
            slippage_tolerance=10,  # Hardcoded default for safety, can be parameterized
            magic_number=self._generate_magic_number(signal.strategy_name)
        )

    def _calculate_position_size(self, equity: float, entry_price: float, stop_loss: float) -> float:
        """
        Calculates the volume in standard lots based on fixed fractional risk.
        Formula: (Equity * Risk_Pct) / (Stop_Loss_Distance * Contract_Size)
        """
        risk_amount = equity * self.risk_per_trade_pct
        sl_distance = abs(entry_price - stop_loss)
        
        if sl_distance <= 0:
            return 0.0
            
        # Raw volume calculation
        raw_volume = risk_amount / (sl_distance * self.contract_size)
        
        # Round down to nearest 0.01 to remain conservative and match MT5 lot stepping
        rounded_volume = int(raw_volume * 100) / 100.0
        
        return rounded_volume

    def _generate_magic_number(self, strategy_name: str) -> int:
        """Generates a deterministic magic number based on the strategy name."""
        return abs(hash(strategy_name)) % (10 ** 8)