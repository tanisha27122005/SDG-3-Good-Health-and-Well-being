import streamlit as st

st.set_page_config(page_title="Wellness Chatbot - MindCare AI", page_icon="🤖", layout="wide")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in from the home page.")
    st.stop()

st.title("🤖 Wellness Assistant & FAQ")
st.markdown("Ask general questions about sleep hygiene, stress management, physical activity, and social support.")

faqs = {
    "How can I improve my sleep?": "To improve sleep hygiene, maintain a consistent sleep schedule, avoid screens 1 hour before bed, keep your room cool, and limit caffeine in the afternoon.",
    "What are quick ways to manage daily stress?": "Try box breathing (4 seconds inhale, 4 hold, 4 exhale, 4 hold), take a short 10-minute walk, or practice mindfulness meditation.",
    "Why is social support important for well-being?": "Strong social connections buffer against stress, improve emotional resilience, and contribute to long-term mental health.",
    "Does this app provide medical advice?": "No. MindCare AI is strictly an educational tool and habit tracker. It does not diagnose, treat, or cure any medical conditions."
}

selected_faq = st.selectbox("Select a common wellness question:", ["-- Choose a question --"] + list(faqs.keys()))

if selected_faq != "-- Choose a question --":
    st.success(faqs[selected_faq])

st.markdown("---")
st.info("💡 **Note:** This is a bounded FAQ-based assistant designed to provide general wellness guidance aligned with UN SDG 3.")