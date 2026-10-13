import pytest
from database import init_db, db_session

def test_database_initialization():
    init_db()
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row["name"] for row in cursor.fetchall()]
        assert "users" in tables
        assert "checkins" in tables
        assert "experiments" in tables
        assert "audit_logs" in tables
