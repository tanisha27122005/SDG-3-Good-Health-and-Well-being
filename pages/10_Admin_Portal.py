import streamlit as st
from admin import get_system_stats, log_audit_action

st.set_page_config(page_title="Admin Portal - MindCare AI", page_icon="🛠️", layout="wide")

if "user" not in st.session_state or st.session_state.user["role"] != "admin":
    st.error("Access Denied. Administrator privileges required.")
    st.stop()

user = st.session_state.user
st.title("🛠️ Administrator Control Panel")

stats = get_system_stats()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Registered Users", stats["total_users"])
with col2:
    st.metric("Total Check-ins", stats["total_checkins"])
with col3:
    st.metric("Total Experiments", stats["total_experiments"])

log_audit_action(user["username"], "VIEW_ADMIN_DASHBOARD", "Viewed system overview stats.")

st.markdown("---")
st.subheader("🔒 Security Audit Logs")
st.dataframe(stats["audit_logs"], use_container_width=True)
