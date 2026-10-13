import streamlit as st
import datetime

st.set_page_config(page_title="Smart AI Health Assistant - MindCare AI", page_icon="🩺", layout="wide")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in from the home page.")
    st.stop()

user = st.session_state.user

st.title("🩺 Smart AI Health Assistant & Clinical Triage")
st.caption("Aligned with UN SDG 3: Good Health and Well-Being")

tab1, tab2 = st.tabs(["📋 Full Clinical Triage & Health Assessment", "💬 Interactive Wellness Chat Assistant"])

with tab1:
    with st.form("advanced_health_form"):
        col1, col2 = st.columns(2)
        with col1:
            sleep_hours = st.number_input("Last Night's Sleep (Hours)", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
            water_intake = st.slider("Daily Water Intake (Glasses)", 0, 16, 6)
            screen_time = st.slider("Daily Screen Time (Hours)", 0, 18, 8)
        with col2:
            stress_level = st.slider("Current Stress Level (1-10)", 1, 10, 4)
            symptoms = st.multiselect(
                "Select active symptoms:",
                [
                    "Mild Fatigue / Low Energy",
                    "Eye Strain / Headache",
                    "Anxiety or Restlessness",
                    "Chest Pain or Shortness of Breath", # Red Flag
                    "Severe Dizziness or Confusion"      # Red Flag
                ]
            )
        submit_btn = st.form_submit_button("Run Analysis")

    if submit_btn:
        st.markdown("---")
        emergencies = [s for s in symptoms if s in ["Chest Pain or Shortness of Breath", "Severe Dizziness or Confusion"]]
        
        if emergencies:
            st.error("🚨 **CRITICAL MEDICAL RED FLAG DETECTED**")
            st.markdown(f"Immediate medical attention required for: `{', '.join(emergencies)}`. Please contact healthcare professionals immediately.")
        else:
            health_score = max(10, 100 - (stress_level * 4) - (len(symptoms) * 8) + int(water_intake * 2))
            st.metric("Calculated Health Score", f"{health_score} / 100")
            st.progress(health_score / 100)
            
            if sleep_hours < 7: st.write("💤 **Advice:** Increase sleep to 7-8 hours to improve recovery.")
            if water_intake < 8: st.write("💧 **Advice:** Drink more water to avoid mental cognitive slowdown.")

with tab2:
    if "assistant_chat" not in st.session_state:
        st.session_state.assistant_chat = [{"role": "assistant", "content": f"Hello {user['username']}! How can I assist your health routine today?"}]
        
    for msg in st.session_state.assistant_chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if prompt := st.chat_input("Ask a question..."):
        st.session_state.assistant_chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        ans = "Focus on 7-8 hours of sleep, 8+ glasses of water, and regular physical breaks throughout the day."
        if "sleep" in prompt.lower(): ans = "Keep your room dark, avoid screen light 1 hour before bed, and maintain a fixed schedule."
        elif "stress" in prompt.lower(): ans = "Practice 4-7-8 breathing exercises and take short 5-minute movement breaks."
        
        st.session_state.assistant_chat.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"): st.write(ans)