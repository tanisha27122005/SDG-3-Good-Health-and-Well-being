import streamlit as st
from services.ml_service import evaluate_model_metrics, load_model

st.set_page_config(page_title="AI/ML Lab - MindCare AI", page_icon="🧪", layout="wide")

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in from the home page.")
    st.stop()

st.title("🧪 AI/ML Lab & Model Evaluation")
st.markdown("Inspect the trained Random Forest educational model trained on synthetic wellness data.")

model = load_model()
if not model:
    st.error("Model file not found. Please run `train_model.py` to generate the model.")
else:
    metrics = evaluate_model_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Accuracy", f"{metrics['accuracy']:.2f}")
    with col2:
        st.metric("Precision", f"{metrics['precision']:.2f}")
    with col3:
        st.metric("Recall", f"{metrics['recall']:.2f}")
    with col4:
        st.metric("F1-Score", f"{metrics['f1']:.2f}")
        
    st.markdown("### Feature Importance")
    st.bar_chart(metrics["feature_importances"])
    
    st.info("ℹ️ **Educational Note:** Model performance metrics reflect synthetic training data distribution and must not be interpreted as clinical diagnoses or real-world medical validation.")
