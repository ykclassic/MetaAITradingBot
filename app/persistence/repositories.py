"""
Implementation of Domain Repository Protocols.
Maps SQLite rows to strongly typed Phase 1 Domain Models.
"""

from typing import List
from uuid import UUID
from datetime import datetime

from app.core.interfaces import TradeRepositoryProtocol
from app.domain.models import Signal, TradeOutcome
from app.domain.enums import SignalDirection, MarketRegime, ExitReason
from app.persistence.database import SQLiteManager


class SQLiteTradeRepository(TradeRepositoryProtocol):
    def __init__(self, db_manager: SQLiteManager):
        self.db = db_manager

    def save_signal(self, signal: Signal) -> None:
        query = """
            INSERT INTO signals (
                signal_id, timestamp, symbol, timeframe, direction,
                entry_price, stop_loss, take_profit, strategy_name,
                strategy_version, signal_confidence, expiration
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self.db.get_connection() as conn:
            conn.execute(query, (
                str(signal.signal_id),
                signal.timestamp.isoformat(),
                signal.symbol,
                signal.timeframe,
                signal.direction.value,
                signal.entry_price,
                signal.stop_loss,
                signal.take_profit,
                signal.strategy_name,
                signal.strategy_version,
                signal.signal_confidence,
                signal.expiration.isoformat()
            ))
            conn.commit()

    def save_trade_outcome(self, outcome: TradeOutcome) -> None:
        query = """
            INSERT INTO trade_outcomes (
                correlation_id, position_id, symbol, strategy_name,
                regime, direction, entry_price, exit_price,
                realized_pnl, r_multiple, holding_seconds,
                exit_reason, closed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self.db.get_connection() as conn:
            conn.execute(query, (
                str(outcome.correlation_id),
                outcome.position_id,
                outcome.symbol,
                outcome.strategy_name,
                outcome.regime.value,
                outcome.direction.value,
                outcome.entry_price,
                outcome.exit_price,
                outcome.realized_pnl,
                outcome.r_multiple,
                outcome.holding_seconds,
                outcome.exit_reason.value,
                outcome.closed_at.isoformat()
            ))
            conn.commit()

    def get_trade_outcomes(self, strategy_name: str, regime: str) -> List[TradeOutcome]:
        query = """
            SELECT * FROM trade_outcomes 
            WHERE strategy_name = ? AND regime = ?
        """
        outcomes = []
        with self.db.get_connection() as conn:
            cursor = conn.execute(query, (strategy_name, regime))
            for row in cursor.fetchall():
                outcomes.append(
                    TradeOutcome(
                        correlation_id=UUID(row["correlation_id"]),
                        position_id=row["position_id"],
                        symbol=row["symbol"],
                        strategy_name=row["strategy_name"],
                        regime=MarketRegime(row["regime"]),
                        direction=SignalDirection(row["direction"]),
                        entry_price=row["entry_price"],
                        exit_price=row["exit_price"],
                        realized_pnl=row["realized_pnl"],
                        r_multiple=row["r_multiple"],
                        holding_seconds=row["holding_seconds"],
                        exit_reason=ExitReason(row["exit_reason"]),
                        closed_at=datetime.fromisoformat(row["closed_at"])
                    )
                )
        return outcomes