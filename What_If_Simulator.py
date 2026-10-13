import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="What-If Simulator - MindCare AI", page_icon="🔮", layout="wide")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in from the home page.")
    st.stop()

st.title("🔮 Predictive What-If Wellness Simulator")
st.markdown("Adjust lifestyle levers below to simulate predicted impact on your daily mood and mental stamina.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Simulated Daily Inputs")
    sim_sleep = st.slider("Simulated Sleep (Hours)", 3.0, 10.0, 7.5, 0.5)
    sim_water = st.slider("Simulated Water Intake (Glasses)", 1, 14, 8)
    sim_exercise = st.slider("Physical Activity (Minutes)", 0, 120, 30, 5)
    sim_screen = st.slider("Screen Time (Hours)", 1, 16, 6)

with col2:
    st.subheader("Predicted Outcomes (SDG 3 Engine)")
    
    # Heuristic simulation formula for demonstration
    base_wellness = 50.0
    sleep_impact = (sim_sleep - 7.0) * 8.0
    water_impact = (sim_water - 6.0) * 3.0
    exercise_impact = (sim_exercise / 30.0) * 10.0
    screen_impact = (8.0 - sim_screen) * 2.5
    
    predicted_score = max(10, min(100, base_wellness + sleep_impact + water_impact + exercise_impact + screen_impact))
    
    st.metric("Predicted Wellness Index", f"{predicted_score:.1f} / 100")
    st.progress(predicted_score / 100)
    
    if predicted_score >= 80:
        st.success("🟢 High Vitality Zone: Excellent balance between rest and movement.")
    elif predicted_score >= 50:
        st.warning("🟡 Moderate Vitality Zone: Pay attention to screen time and hydration.")
    else:
        st.error("🔴 High Fatigue Zone: Increased risk of burnout and low concentration.")

st.markdown("---")
st.caption("Note: This simulation uses non-clinical predictive heuristic modeling for academic lifestyle awareness.")