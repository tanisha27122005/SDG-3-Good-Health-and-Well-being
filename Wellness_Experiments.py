import streamlit as st
from datetime import date
from services.wellness_service import add_experiment, get_user_experiments

st.set_page_config(page_title="Wellness Experiments - MindCare AI", page_icon="🧪", layout="wide")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in from the home page.")
    st.stop()

user = st.session_state.user
st.title("🧪 Personal Wellness Experiments")
st.markdown("Test a habit change (e.g., 7 days of meditation or no screens before bed) and track its impact.")

with st.form("experiment_form"):
    habit_name = st.text_input("Habit / Routine Change Name", placeholder="e.g., 30 mins morning walk")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today())
    with col2:
        end_date = st.date_input("End Date", value=date.today())
        
    pre_mood = st.slider("Mood Before Habit (1-10)", 1, 10, 5)
    post_mood = st.slider("Mood After Habit (1-10)", 1, 10, 7)
    notes = st.text_area("Experiment Notes & Observations", placeholder="How did you feel during this routine change?")
    
    submitted = st.form_submit_button("Save Experiment")
    if submitted:
        if not habit_name.strip():
            st.error("Please enter a valid habit name.")
        else:
            add_experiment(user["id"], habit_name, str(start_date), str(end_date), pre_mood, post_mood, notes)
            st.success("Experiment recorded successfully!")
            st.rerun()

st.markdown("---")
st.subheader("Your Past Experiments")
df_exp = get_user_experiments(user["id"])

if df_exp is None or df_exp.empty:
    st.info("No experiments recorded yet.")
else:
    st.dataframe(df_exp, width="stretch")