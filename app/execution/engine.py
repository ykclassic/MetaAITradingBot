"""
Execution Engine.
Responsible for idempotency checks, executing trades via the adapter, and handling exceptions safely.
"""

import logging
from typing import Optional, Set
from datetime import datetime, timezone

from app.core.interfaces import MarketDataAdapter
from app.domain.models import OrderRequest, OrderResult
from app.domain.enums import OrderExecutionState

logger = logging.getLogger(__name__)


class ExecutionEngine:
    """
    Safely executes orders and tracks idempotency to prevent duplicate trades.
    """
    
    def __init__(self, adapter: MarketDataAdapter):
        self.adapter = adapter
        # In-memory idempotency cache. In production, this should be distributed (e.g., Redis).
        self._processed_requests: Set[str] = set()

    def execute_order(self, request: OrderRequest) -> OrderResult:
        """
        Attempts to execute the order safely, ensuring it hasn't been processed before.
        """
        if request.idempotency_key in self._processed_requests:
            logger.warning(f"Duplicate order request blocked. Key: {request.idempotency_key}")
            return self._build_failed_result(
                request, 
                OrderExecutionState.REJECTED_BY_BROKER, 
                "Idempotency key already processed."
            )

        # Mark as processed immediately to prevent race conditions in tight loops
        self._processed_requests.add(request.idempotency_key)

        try:
            logger.info(f"Sending {request.direction.value} order for {request.volume} {request.symbol} to adapter.")
            result = self.adapter.send_order(request)
            
            self._log_execution_result(result)
            return result
            
        except Exception as e:
            logger.error(f"Critical failure during order execution: {str(e)}", exc_info=True)
            return self._build_failed_result(
                request,
                OrderExecutionState.EXECUTION_UNCERTAIN,
                f"Unhandled exception during adapter call: {str(e)}"
            )

    def _build_failed_result(self, request: OrderRequest, state: OrderExecutionState, message: str) -> OrderResult:
        """Helper to construct deterministic failure results."""
        return OrderResult(
            idempotency_key=request.idempotency_key,
            correlation_id=request.correlation_id,
            mt5_ticket=None,
            execution_state=state,
            fill_price=0.0,
            filled_volume=0.0,
            executed_at=datetime.now(timezone.utc),
            error_message=message
        )

    def _log_execution_result(self, result: OrderResult) -> None:
        """Centralized logging for execution outcomes."""
        if result.execution_state == OrderExecutionState.FILLED:
            logger.info(
                f"Trade FILLED successfully. Ticket: {result.mt5_ticket}, "
                f"Price: {result.fill_price}, Volume: {result.filled_volume}"
            )
        elif result.execution_state == OrderExecutionState.EXECUTION_UNCERTAIN:
            logger.critical(
                f"EXECUTION UNCERTAIN. Adapter failed to confirm trade status. "
                f"Manual intervention required. Details: {result.error_message}"
            )
        else:
            logger.warning(
                f"Trade REJECTED. Reason: {result.error_message}"
            )