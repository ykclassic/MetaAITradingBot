"""
SQLite Database Connection and Schema Management.
Ensures thread-safe connections and schema initialization.
"""

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from uuid import uuid4

logger = logging.getLogger(__name__)


class SQLiteManager:
    def __init__(self, db_path: str = "data/trading_system.sqlite"):
        self._is_memory = db_path == ":memory:"
        if self._is_memory:
            # Keep one anchor connection alive so all connections belonging to
            # this manager share the same in-memory database. Each manager gets
            # a unique URI, preventing state from leaking between test cases.
            self.db_path = f"file:trading_system_test_{uuid4().hex}?mode=memory&cache=shared"
            self._uri = True
            self._anchor = sqlite3.connect(self.db_path, uri=True)
            self._anchor.row_factory = sqlite3.Row
        else:
            self.db_path = Path(db_path)
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._uri = False
            self._anchor = None

        self._initialize_schema()

    def _initialize_schema(self) -> None:
        """Loads and executes the schema.sql file on the active database."""
        schema_path = Path(__file__).parent / "schema.sql"
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found at {schema_path}")

        with open(schema_path, "r") as f:
            schema_script = f.read()

        try:
            if self._is_memory:
                self._anchor.executescript(schema_script)
                self._anchor.commit()
            else:
                with sqlite3.connect(self.db_path) as conn:
                    conn.executescript(schema_script)
                    conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize database schema: {e}")
            raise

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Provides a context-managed database connection."""
        conn = sqlite3.connect(
            self.db_path,
            uri=self._uri,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Database error during transaction: {e}")
            raise
        finally:
            conn.close()

    def close(self) -> None:
        """Release the shared in-memory anchor connection."""
        if self._anchor is not None:
            self._anchor.close()
            self._anchor = None
