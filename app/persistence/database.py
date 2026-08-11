"""
SQLite Database Connection and Schema Management.
Ensures thread-safe connections and schema initialization.
"""

import sqlite3
import logging
from pathlib import Path
from contextlib import contextmanager
from typing import Generator

logger = logging.getLogger(__name__)

class SQLiteManager:
    def __init__(self, db_path: str = "data/trading_system.sqlite"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        """Loads and executes the schema.sql file if tables don't exist."""
        schema_path = Path(__file__).parent / "schema.sql"
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found at {schema_path}")
            
        with open(schema_path, "r") as f:
            schema_script = f.read()

        try:
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
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        conn.row_factory = sqlite3.Row  # Returns rows as dict-like objects
        try:
            yield conn
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Database error during transaction: {e}")
            raise
        finally:
            conn.close()