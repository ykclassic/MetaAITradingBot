"""Verify authenticated XT spot balances without exposing credentials."""

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Allow direct execution as `python scripts/verify_xt_account.py` from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.data.xt_adapter import XTAdapter


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main() -> int:
    load_dotenv()
    api_key = os.environ.get("XT_API_KEY", "")
    secret_key = os.environ.get("XT_SECRET_KEY", "")
    if not api_key or not secret_key:
        logger.error("XT credentials are missing")
        return 1

    adapter = XTAdapter(api_key=api_key, secret_key=secret_key)
    try:
        if not adapter.connect():
            logger.error("XT authentication/connectivity check failed")
            return 1

        balances = adapter.get_account_balances()
        logger.info("XT ACCOUNT AUTHENTICATION: PASS")
        logger.info("XT BALANCE ASSET COUNT: %d", len(balances))

        usdt = balances.get("usdt")
        if usdt is None:
            logger.warning("XT USDT BALANCE: NOT PRESENT IN /v4/balances RESPONSE")
        else:
            logger.info(
                "XT USDT BALANCE: available=%s frozen=%s total=%s",
                usdt["available"],
                usdt["frozen"],
                usdt["total"],
            )

        for currency in sorted(balances):
            asset = balances[currency]
            if asset["total"] != 0.0:
                logger.info(
                    "XT NONZERO ASSET: currency=%s available=%s frozen=%s total=%s",
                    currency,
                    asset["available"],
                    asset["frozen"],
                    asset["total"],
                )
        return 0
    except Exception:
        logger.exception("XT account balance verification failed")
        return 1
    finally:
        adapter.disconnect()


if __name__ == "__main__":
    sys.exit(main())
