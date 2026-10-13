import streamlit as st
from datetime import date
from services.wellness_service import add_checkin

st.set_page_config(page_title="Daily Check-in - MindCare AI", page_icon="📝", layout="wide")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in from the home page.")
    st.stop()

user = st.session_state.user
st.title("📝 Daily Wellness Check-in")

with st.form("checkin_form"):
    check_date = st.date_input("Check-in Date", value=date.today())
    mood = st.slider("Mood Rating (1 = Very Low, 10 = Excellent)", 1, 10, 7)
    stress = st.slider("Stress Level (1 = None, 10 = Extremely High)", 1, 10, 3)
    sleep = st.number_input("Sleep Duration (Hours)", min_value=0.0, max_value=24.0, value=7.5, step=0.5)
    energy = st.slider("Energy Level (1 = Exhausted, 10 = High Energy)", 1, 10, 7)
    social = st.slider("Perceived Social Support (1 = Isolated, 10 = Well Supported)", 1, 10, 7)
    activity = st.selectbox("Primary Daily Activity", ["Exercise", "Work / Study", "Meditation / Mindfulness", "Socializing", "Rest / Relaxation", "Other"])
    journal = st.text_area("Optional Journal Entry (Private)", placeholder="Reflect on your day...")
    
    submitted = st.form_submit_button("Save Check-in")
    if submitted:
        add_checkin(user["id"], str(check_date), mood, stress, sleep, energy, social, activity, journal)
        st.success("Daily check-in saved successfully!")
