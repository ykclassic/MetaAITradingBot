"""Execution engine for broker order submission and idempotency."""

import logging
from datetime import datetime, timezone
from typing import Set

from app.core.interfaces import MarketDataAdapter
from app.domain.enums import OrderExecutionState
from app.domain.models import OrderRequest, OrderResult

logger = logging.getLogger(__name__)


class ExecutionEngine:
    """Safely executes orders and makes every execution gate observable."""

    def __init__(self, adapter: MarketDataAdapter, live_trading_enabled: bool = True):
        self.adapter = adapter
        self.live_trading_enabled = live_trading_enabled
        self._processed_requests: Set[str] = set()

    def execute_order(self, request: OrderRequest) -> OrderResult:
        """Execute an order only when live trading is explicitly enabled."""
        if request.idempotency_key in self._processed_requests:
            logger.warning("EXECUTION BLOCKED: duplicate idempotency key=%s", request.idempotency_key)
            return self._build_failed_result(
                request,
                OrderExecutionState.REJECTED_BY_BROKER,
                "Idempotency key already processed.",
            )

        self._processed_requests.add(request.idempotency_key)

        if not self.live_trading_enabled:
            logger.warning(
                "EXECUTION GATE REACHED: LIVE_TRADING_ENABLED=false; "
                "XT order submission intentionally skipped."
            )
            return self._build_failed_result(
                request,
                OrderExecutionState.CANCELLED,
                "Live trading disabled by configuration.",
            )

        logger.info(
            "XT ORDER SUBMISSION START: side=%s symbol=%s quantity=%s price=%s correlation_id=%s",
            request.direction.value,
            request.symbol,
            request.volume,
            request.price,
            request.correlation_id,
        )

        try:
            result = self.adapter.send_order(request)
            self._log_execution_result(result)
            return result
        except Exception as exc:
            logger.error("XT order submission raised an unexpected exception", exc_info=True)
            return self._build_failed_result(
                request,
                OrderExecutionState.EXECUTION_UNCERTAIN,
                f"Unhandled exception during adapter call: {exc}",
            )

    def _build_failed_result(
        self, request: OrderRequest, state: OrderExecutionState, message: str
    ) -> OrderResult:
        return OrderResult(
            idempotency_key=request.idempotency_key,
            correlation_id=request.correlation_id,
            order_id=None,
            execution_state=state,
            fill_price=0.0,
            filled_volume=0.0,
            executed_at=datetime.now(timezone.utc),
            error_message=message,
        )

    def _log_execution_result(self, result: OrderResult) -> None:
        if result.execution_state == OrderExecutionState.FILLED:
            logger.info(
                "TRADE FILLED: order_id=%s price=%s volume=%s",
                result.order_id,
                result.fill_price,
                result.filled_volume,
            )
        elif result.execution_state == OrderExecutionState.IN_FLIGHT:
            logger.info("XT ORDER ACCEPTED: order_id=%s; awaiting fill confirmation", result.order_id)
        elif result.execution_state == OrderExecutionState.EXECUTION_UNCERTAIN:
            logger.critical(
                "EXECUTION UNCERTAIN: XT did not confirm final order state. Details: %s",
                result.error_message,
            )
        else:
            logger.warning("TRADE REJECTED/CANCELLED: %s", result.error_message)
