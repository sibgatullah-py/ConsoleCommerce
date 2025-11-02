import sqlite3
import os
from datetime import datetime
import hashlib

class DatabaseManager:
    """
    High-level wrapper for SQLite database operations.
    Handles initialization, table creation, query execution,
    and safe admin bootstrapping.
    """

    def __init__(self, db_path: str = "data/ecommerce.db"):
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # access results by column name
        self.cursor = self.conn.cursor()

        # Initialize tables and default admin
        self._create_tables()
        self._create_default_admin()

    # ------------ Table Creation ------------
    def _create_tables(self):
        """Create all required tables if they do not already exist."""

        # Users
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'customer',
                created_at TEXT
            )
        """)

        # Products
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                description TEXT
            )
        """)

        # Orders
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                items_json TEXT,
                status TEXT,
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        self.conn.commit()

    # ------------ Default Admin Creation ------------
    def _create_default_admin(self):
        """Bootstrap a default admin account if none exists."""
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        admin_count = self.cursor.fetchone()[0]

        if admin_count == 0:
            print("🛠 Creating default admin account...")

            username = "admin"
            password = "admin123"  # In real apps, hash this!
            created_at = datetime.now().isoformat(timespec="seconds")

            self.cursor.execute("""
                INSERT INTO users (username, password, role, created_at)
                VALUES (?, ?, 'admin', ?)
            """, (username, password, created_at))
            self.conn.commit()

            print("✅ Default admin created! (username: admin, password: admin123)")

    # ------------ General Query Execution ------------
    def execute(self, query: str, params: tuple = (), fetchone=False, fetchall=False, commit=False):
        """Execute an SQL query safely with parameters."""
        try:
            self.cursor.execute(query, params)
            if commit:
                self.conn.commit()
            if fetchone:
                return self.cursor.fetchone()
            if fetchall:
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return None

    # Optional helper wrappers
    def fetch_one(self, query, params=()):
        return self.execute(query, params, fetchone=True)

    def fetch_all(self, query, params=()):
        return self.execute(query, params, fetchall=True)

    # ------------ Context Manager Support ------------
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ------------ Connection Close ------------
    def close(self):
        """Close database connection safely."""
        if self.conn:
            self.conn.close()
