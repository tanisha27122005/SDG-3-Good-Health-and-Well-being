from database import db_session

def log_audit_action(admin_username: str, action: str, details: str = ""):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO audit_logs (admin_username, action, details) VALUES (?, ?, ?)",
            (admin_username, action, details)
        )

def get_system_stats():
    with db_session() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM users")
        total_users = cursor.fetchone()["count"]
        
        cursor.execute("SELECT COUNT(*) as count FROM checkins")
        total_checkins = cursor.fetchone()["count"]
        
        cursor.execute("SELECT COUNT(*) as count FROM experiments")
        total_experiments = cursor.fetchone()["count"]
        
        cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 50")
        audit_logs = [dict(row) for row in cursor.fetchall()]
        
    return {
        "total_users": total_users,
        "total_checkins": total_checkins,
        "total_experiments": total_experiments,
        "audit_logs": audit_logs
    }