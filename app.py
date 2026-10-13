
import streamlit as st
import hashlib
import sqlite3

from database import init_db, db_session, create_default_admin

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MindCare AI | SDG 3",
    page_icon="🧠",
    layout="wide"
)

# ---------------- DATABASE SETUP ----------------
init_db()
create_default_admin()

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- PASSWORD ----------------
def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ---------------- LOGIN ----------------
def authenticate_user(username, password):
    password_hash = hash_password(password)

    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, username, role
            FROM users
            WHERE username = ? AND password_hash = ?
            """,
            (username.strip(), password_hash)
        )
        row = cursor.fetchone()

        if row:
            return dict(row)

    return None


# ---------------- USER REGISTRATION ----------------
def register_user(username, password):
    username = username.strip()

    if len(username) < 3:
        return False, "Username must contain at least 3 characters."

    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    try:
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, 'user')
                """,
                (username, hash_password(password))
            )
        return True, "Account created. Please log in."

    except sqlite3.IntegrityError:
        return False, "Username already exists."

    except sqlite3.Error:
        return False, "Database error. Check the users table."


# ---------------- LOGIN / REGISTER SCREEN ----------------
if st.session_state.user is None:
    st.title("🧠 MindCare AI")
    st.subheader("SDG 3 — Good Health and Well-being")
    st.write("Your personal wellness tracking and AI/ML learning portal.")

    login_tab, register_tab = st.tabs(["🔐 Login", "📝 Register"])

    with login_tab:
        st.subheader("Login to MindCare AI")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_clicked = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if login_clicked:
            if not username.strip() or not password:
                st.warning("Enter both username and password.")
            else:
                user = authenticate_user(username, password)

                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with st.expander("Admin login details"):
            st.write("Username: `admin`")
            st.write("Password: `MindCare@2026`")
            st.caption(
                "Change the default password before deploying the app publicly."
            )

    with register_tab:
        st.subheader("Create a User Account")

        with st.form("register_form"):
            new_username = st.text_input("Choose username")
            new_password = st.text_input(
                "Choose password",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password"
            )
            register_clicked = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

        if register_clicked:
            if new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message = register_user(
                    new_username,
                    new_password
                )

                if success:
                    st.success(message)
                else:
                    st.error(message)

    st.stop()


# ---------------- AUTHENTICATED DASHBOARD ----------------
user = st.session_state.user

# Extra safety check for session data
if not isinstance(user, dict):
    st.session_state.user = None
    st.rerun()

role = str(user.get("role", "user")).lower()

st.sidebar.title("🧠 MindCare AI")
st.sidebar.write(f"**User:** {user.get('username', 'Unknown')}")
st.sidebar.write(f"**Role:** {role.upper()}")
st.sidebar.divider()

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.user = None
    st.rerun()

st.title("🌿 MindCare AI Dashboard")
st.caption("SDG 3: Good Health and Well-being")

if role == "admin":
    st.subheader("Administrator Dashboard")
    st.write("Manage and monitor application activity.")

    try:
        with db_session() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM checkins")
            total_checkins = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM experiments")
            total_experiments = cursor.fetchone()[0]

        c1, c2, c3 = st.columns(3)
        c1.metric("Registered Accounts", total_users)
        c2.metric("Wellness Check-ins", total_checkins)
        c3.metric("Experiments", total_experiments)

    except sqlite3.Error as error:
        st.warning(f"Dashboard statistics unavailable: {error}")

    st.info(
        "Use the Admin Portal page in the sidebar to access "
        "administrative features."
    )

else:
    st.subheader(f"Welcome, {user.get('username', 'User')}!")

    st.write(
        "Track daily wellness, review personal progress, "
        "and explore lifestyle experiments."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "**📋 Daily Check-in**\n\n"
            "Record mood, stress, sleep and energy."
        )

    with col2:
        st.success(
            "**🧪 Wellness Experiments**\n\n"
            "Track lifestyle experiments and their outcomes."
        )

    with col3:
        st.warning(
            "**🤖 AI/ML Wellness Lab**\n\n"
            "Explore model-based wellness insights."
        )

    st.caption(
        "This educational application is not a substitute "
        "for professional mental-health care."
    )
