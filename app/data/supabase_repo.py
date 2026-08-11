"""
Cloud State Persistence via Supabase.
Cures server amnesia by storing idempotency keys and execution states in PostgreSQL.
"""

import logging
from typing import Optional
from supabase import create_client, Client
from app.domain.models import OrderResult
from app.domain.enums import OrderExecutionState

logger = logging.getLogger(__name__)

class ExecutionRepository:
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def log_execution(self, result: OrderResult) -> bool:
        """Persists the OrderResult to the Supabase PostgreSQL database."""
        try:
            payload = {
                "idempotency_key": result.idempotency_key,
                "correlation_id": str(result.correlation_id),
                "broker_order_id": str(result.mt5_ticket) if result.mt5_ticket else None,
                "execution_state": result.execution_state.value,
                "fill_price": result.fill_price,
                "filled_volume": result.filled_volume,
                "executed_at": result.executed_at.isoformat(),
                "error_message": result.error_message
            }
            
            # Using upsert to handle potential network retry collisions gracefully
            response = self.supabase.table("execution_logs").upsert(payload).execute()
            
            if len(response.data) > 0:
                logger.debug(f"Execution {result.idempotency_key} securely logged to Supabase.")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to persist execution state to Supabase: {e}", exc_info=True)
            return False

    def is_idempotency_key_processed(self, idempotency_key: str) -> bool:
        """Checks permanent storage to see if an order was already processed."""
        try:
            response = self.supabase.table("execution_logs") \
                .select("idempotency_key") \
                .eq("idempotency_key", idempotency_key) \
                .execute()
                
            return len(response.data) > 0
        except Exception as e:
            logger.error(f"Failed to query Supabase for idempotency key: {e}")
            # Fail closed: If we can't verify the DB, we assume it WAS processed to prevent double-buys.
            return True