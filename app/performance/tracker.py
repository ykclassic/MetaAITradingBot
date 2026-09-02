"""Persistent trading journal and performance analytics backed by SQLite."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Optional
from uuid import UUID

from app.domain.models import OrderResult, Signal, TradeOutcome
from app.persistence.database import SQLiteManager


@dataclass(frozen=True)
class PerformanceMetrics:
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate_pct: float
    net_pnl: float
    gross_profit: float
    gross_loss: float
    profit_factor: Optional[float]
    expectancy: float
    average_win: float
    average_loss: float
    average_r_multiple: float
    max_drawdown: float
    best_trade: float
    worst_trade: float
    average_holding_seconds: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PerformanceTracker:
    """Record every important trading decision and calculate journal metrics."""

    def __init__(self, db_manager: SQLiteManager):
        self.db = db_manager
        self._initialize_tables()

    def _initialize_tables(self) -> None:
        with self.db.get_connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS journal_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_time TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    symbol TEXT,
                    correlation_id TEXT,
                    strategy_name TEXT,
                    direction TEXT,
                    price REAL,
                    quantity REAL,
                    pnl REAL,
                    r_multiple REAL,
                    execution_state TEXT,
                    order_id INTEGER,
                    details_json TEXT NOT NULL DEFAULT '{}'
                );
                CREATE INDEX IF NOT EXISTS idx_journal_time ON journal_events(event_time);
                CREATE INDEX IF NOT EXISTS idx_journal_symbol ON journal_events(symbol, event_time);
                CREATE INDEX IF NOT EXISTS idx_journal_type ON journal_events(event_type, event_time);
                """
            )
            conn.commit()

    def record_event(
        self,
        event_type: str,
        *,
        symbol: Optional[str] = None,
        correlation_id: Optional[UUID | str] = None,
        strategy_name: Optional[str] = None,
        direction: Optional[str] = None,
        price: Optional[float] = None,
        quantity: Optional[float] = None,
        pnl: Optional[float] = None,
        r_multiple: Optional[float] = None,
        execution_state: Optional[str] = None,
        order_id: Optional[int] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        with self.db.get_connection() as conn:
            conn.execute(
                """INSERT INTO journal_events (
                    event_time, event_type, symbol, correlation_id, strategy_name,
                    direction, price, quantity, pnl, r_multiple, execution_state,
                    order_id, details_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    datetime.now(timezone.utc).isoformat(), event_type, symbol,
                    str(correlation_id) if correlation_id else None, strategy_name,
                    direction, price, quantity, pnl, r_multiple, execution_state,
                    order_id, json.dumps(details or {}, default=str, sort_keys=True),
                ),
            )
            conn.commit()

    def record_signal(self, signal: Signal, regime: Optional[str] = None) -> None:
        self.record_event(
            "SIGNAL",
            symbol=signal.symbol,
            correlation_id=signal.signal_id,
            strategy_name=signal.strategy_name,
            direction=signal.direction.value,
            price=signal.entry_price,
            details={
                "timeframe": signal.timeframe,
                "stop_loss": signal.stop_loss,
                "take_profit": signal.take_profit,
                "confidence": signal.signal_confidence,
                "expiration": signal.expiration.isoformat(),
                "regime": regime,
            },
        )

    def record_execution(self, result: OrderResult, symbol: str) -> None:
        self.record_event(
            "EXECUTION",
            symbol=symbol,
            correlation_id=result.correlation_id,
            price=result.fill_price,
            quantity=result.filled_volume,
            execution_state=result.execution_state.value,
            order_id=result.order_id,
            details={"error": result.error_message},
        )

    def record_trade_outcome(self, outcome: TradeOutcome) -> None:
        self.record_event(
            "TRADE_CLOSED",
            symbol=outcome.symbol,
            correlation_id=outcome.correlation_id,
            strategy_name=outcome.strategy_name,
            direction=outcome.direction.value,
            price=outcome.exit_price,
            pnl=outcome.realized_pnl,
            r_multiple=outcome.r_multiple,
            details={
                "position_id": outcome.position_id,
                "entry_price": outcome.entry_price,
                "holding_seconds": outcome.holding_seconds,
                "exit_reason": outcome.exit_reason.value,
                "closed_at": outcome.closed_at.isoformat(),
            },
        )

    def record_cycle(self, duration_seconds: float, symbols: Iterable[str], signals: int, approved: int, executions: int) -> None:
        self.record_event(
            "CYCLE",
            details={
                "duration_seconds": duration_seconds,
                "symbols": list(symbols),
                "signals": signals,
                "risk_approved": approved,
                "executions": executions,
            },
        )

    def get_metrics(self, since: Optional[datetime] = None) -> PerformanceMetrics:
        where = "WHERE event_type = 'TRADE_CLOSED'"
        params: list[Any] = []
        if since:
            where += " AND event_time >= ?"
            params.append(since.astimezone(timezone.utc).isoformat())

        with self.db.get_connection() as conn:
            rows = conn.execute(
                f"SELECT pnl, r_multiple, details_json FROM journal_events {where} ORDER BY event_time ASC",
                params,
            ).fetchall()

        pnls = [float(row["pnl"]) for row in rows if row["pnl"] is not None]
        rs = [float(row["r_multiple"]) for row in rows if row["r_multiple"] is not None]
        holds = []
        for row in rows:
            try:
                value = json.loads(row["details_json"]).get("holding_seconds")
                if value is not None:
                    holds.append(float(value))
            except (TypeError, ValueError, json.JSONDecodeError):
                continue

        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p < 0]
        gross_profit = sum(wins)
        gross_loss = abs(sum(losses))
        equity = peak = max_drawdown = 0.0
        for pnl in pnls:
            equity += pnl
            peak = max(peak, equity)
            max_drawdown = max(max_drawdown, peak - equity)

        # Profit factor is undefined when no losing trade exists, so expose it as null.
        profit_factor = gross_profit / gross_loss if gross_loss else None
        expectancy = sum(pnls) / len(pnls) if pnls else 0.0
        return PerformanceMetrics(
            total_trades=len(pnls),
            winning_trades=len(wins),
            losing_trades=len(losses),
            win_rate_pct=(len(wins) / len(pnls) * 100.0) if pnls else 0.0,
            net_pnl=sum(pnls),
            gross_profit=gross_profit,
            gross_loss=gross_loss,
            profit_factor=profit_factor,
            expectancy=expectancy,
            average_win=(gross_profit / len(wins)) if wins else 0.0,
            average_loss=(sum(losses) / len(losses)) if losses else 0.0,
            average_r_multiple=(sum(rs) / len(rs)) if rs else 0.0,
            max_drawdown=max_drawdown,
            best_trade=max(pnls) if pnls else 0.0,
            worst_trade=min(pnls) if pnls else 0.0,
            average_holding_seconds=(sum(holds) / len(holds)) if holds else 0.0,
        )
