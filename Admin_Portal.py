import streamlit as st
from admin import get_system_stats, log_audit_action

st.set_page_config(page_title="Admin Portal - MindCare AI", page_icon="🛠️", layout="wide")

# Safe session & role validation
user = st.session_state.get("user")

if not user:
    st.error("Please log in first to access this page.")
    st.stop()

if isinstance(user, dict) and user.get("role") != "admin":
    st.error("Access Denied. Administrator privileges required.")
    st.stop()

st.title("🛠️ System Control Panel")

# Fetch system stats safely
stats = get_system_stats()

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Registered Users", stats.get("total_users", 0))
with c2:
    st.metric("Total Check-ins", stats.get("total_checkins", 0))
with c3:
    st.metric("Active Experiments", stats.get("total_experiments", 0))

# Log admin activity
username = user.get("username", "admin")
log_audit_action(username, "VIEW_ADMIN_DASHBOARD", "Opened system overview.")

st.markdown("---")
st.subheader("🔒 Audit Trail Logs")

audit_logs = stats.get("audit_logs")
if audit_logs is not None and not audit_logs.empty:
    st.dataframe(audit_logs, use_container_width=True)
else:
    st.info("No audit logs found.")