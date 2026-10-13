
import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data.db"


def get_user_checkins(user_id, days=30):
    """Fetch check-ins for a user within the requested period."""
    try:
        days = max(1, int(days))
    except (TypeError, ValueError):
        days = 30

    if not DB_PATH.exists():
        return pd.DataFrame()

    with sqlite3.connect(str(DB_PATH), timeout=10) as conn:
        columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(checkins)")
        }

        if not columns or "user_id" not in columns:
            return pd.DataFrame()

        date_column = (
            "created_at" if "created_at" in columns
            else "date" if "date" in columns
            else None
        )

        if date_column:
            query = f"""
                SELECT *
                FROM checkins
                WHERE user_id = ?
                  AND date("{date_column}") >=
                      date('now', '-' || ? || ' days')
                ORDER BY date("{date_column}") ASC
            """
            return pd.read_sql_query(
                query, conn, params=(user_id, days)
            )

        order = "id" if "id" in columns else "rowid"
        return pd.read_sql_query(
            f'SELECT * FROM checkins WHERE user_id = ? ORDER BY "{order}"',
            conn,
            params=(user_id,)
        )


def add_checkin(
    user_id,
    check_date,
    mood,
    stress,
    sleep,
    energy,
    social,
    activity,
    journal
):
    """Save a daily check-in using columns available in data.db."""

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    with sqlite3.connect(str(DB_PATH), timeout=10) as conn:
        columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(checkins)")
        }

        if not columns:
            raise ValueError(
                "The checkins table does not exist. Initialize the database first."
            )

        if "user_id" not in columns:
            raise ValueError(
                "The checkins table is missing the user_id column."
            )

        # Map form fields to common database column names.
        values = {
            "user_id": user_id,
            "date": str(check_date),
            "created_at": str(check_date),
            "mood": mood,
            "stress": stress,
            "sleep_hours": sleep,
            "sleep": sleep,
            "energy": energy,
            "support": social,
            "social": social,
            "activity": activity,
            "journal": journal,
            "journal_entry": journal,
        }

        # Prefer one date column if both exist.
        if "created_at" in columns and "date" in columns:
            values.pop("date")

        insert_values = {
            key: value
            for key, value in values.items()
            if key in columns
        }

        if "mood" not in insert_values:
            raise ValueError(
                "The checkins table is missing the mood column."
            )

        names = ", ".join(
            '"' + name.replace('"', '""') + '"'
            for name in insert_values
        )
        placeholders = ", ".join("?" for _ in insert_values)

        conn.execute(
            f"INSERT INTO checkins ({names}) VALUES ({placeholders})",
            tuple(insert_values.values())
        )
