import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Project folder and database path
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data.db"


@contextmanager
def db_session():
    """Open a database connection and manage transactions."""
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create required tables without deleting existing data."""
    with db_session() as conn:

        # Users and login
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            )
        """)

        # Daily wellness check-ins
        conn.execute("""
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                mood TEXT,
                stress INTEGER,
                sleep_hours REAL,
                energy INTEGER,
                support TEXT,
                activity TEXT,
                journal TEXT
            )
        """)

        # Wellness experiments
        conn.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                experiment_name TEXT,
                baseline_value REAL,
                result_value REAL,
                notes TEXT
            )
        """)

        # Admin audit history
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                admin_username TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                action TEXT,
                details TEXT
            )
        """)

        # Add missing columns to existing tables.
        # Existing records are preserved.
        required_columns = {
            "users": {
                "username": "TEXT",
                "password_hash": "TEXT",
                "role": "TEXT DEFAULT 'user'"
            },
            "checkins": {
                "user_id": "INTEGER",
                "created_at": "TEXT",
                "mood": "TEXT",
                "stress": "INTEGER",
                "sleep_hours": "REAL",
                "energy": "INTEGER",
                "support": "TEXT",
                "activity": "TEXT",
                "journal": "TEXT"
            },
            "experiments": {
                "user_id": "INTEGER",
                "created_at": "TEXT",
                "experiment_name": "TEXT",
                "baseline_value": "REAL",
                "result_value": "REAL",
                "notes": "TEXT"
            },
            "audit_logs": {
                "user_id": "INTEGER",
                "admin_username": "TEXT",
                "created_at": "TEXT",
                "timestamp": "TEXT",
                "action": "TEXT",
                "details": "TEXT"
            }
        }

        for table, definitions in required_columns.items():
            existing = {
                row[1]
                for row in conn.execute(
                    f'PRAGMA table_info("{table}")'
                )
            }

            for column, definition in definitions.items():
                if column not in existing:
                    conn.execute(
                        f'ALTER TABLE "{table}" '
                        f'ADD COLUMN "{column}" {definition}'
                    )


def get_db_path():
    """Return the database file path."""
    return str(DB_PATH)


def get_system_stats():
    """Return admin dashboard statistics."""
    with db_session() as conn:
        return {
            "total_users": conn.execute(
                "SELECT COUNT(*) FROM users"
            ).fetchone()[0],
            "total_checkins": conn.execute(
                "SELECT COUNT(*) FROM checkins"
            ).fetchone()[0],
            "total_experiments": conn.execute(
                "SELECT COUNT(*) FROM experiments"
            ).fetchone()[0],
            "total_audit_logs": conn.execute(
                "SELECT COUNT(*) FROM audit_logs"
            ).fetchone()[0]
        }


def log_audit_action(user_id=None, action="", details="",
                     admin_username=None):
    """Record an administrative or system action."""
    with db_session() as conn:
        conn.execute("""
            INSERT INTO audit_logs
                (user_id, admin_username, action, details)
            VALUES (?, ?, ?, ?)
        """, (user_id, admin_username, action, details))


def ensure_user_columns():
    """Ensure login columns exist in the users table."""
    init_db()
    
def create_default_admin():
    import hashlib
    import sqlite3

    username = "admin"
    password = "MindCare@2026"
    password_hash = hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()

    with db_session() as conn:
        cursor = conn.cursor()

        # Check whether the admin username already exists
        cursor.execute(
            "SELECT id, role FROM users WHERE username = ?",
            (username,)
        )
        existing = cursor.fetchone()

        if existing is None:
            cursor.execute(
                """
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
                """,
                (username, password_hash, "admin")
            )
        elif existing["role"] != "admin":
            # Do not silently change an existing user's role
            raise ValueError(
                "Username 'admin' already exists but is not an admin. "
                "Use a different admin username or verify the account."
            )
