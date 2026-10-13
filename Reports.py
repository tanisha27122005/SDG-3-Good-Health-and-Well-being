import streamlit as st
from services.wellness_service import get_user_checkins
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

st.set_page_config(page_title="Reports & Export - MindCare AI", page_icon="📄", layout="wide")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in from the home page.")
    st.stop()

user = st.session_state.user
st.title("📄 Wellness Reports & Data Export")

df = get_user_checkins(user["id"], days=90)

if df.empty:
    st.info("No check-in records available for export.")
else:
    st.subheader("Export Check-in Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV Report",
        data=csv,
        file_name=f"mindcare_report_{user['username']}.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    st.subheader("Download Summary PDF")
    if st.button("Generate PDF Report"):
        pdf_path = f"mindcare_report_{user['username']}.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        story.append(Paragraph(f"MindCare AI - Wellness Summary Report", styles['Title']))
        story.append(Paragraph(f"User: {user['username']}", styles['Heading2']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Total Check-ins recorded: {len(df)}", styles['Normal']))
        story.append(Paragraph(f"Average Mood: {df['mood'].mean():.1f}/10", styles['Normal']))
        story.append(Paragraph(f"Average Sleep: {df['sleep'].mean():.1f} hours", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Aligned with UN SDG 3: Good Health and Well-Being", styles['Italic']))
        
        doc.build(story)
        
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download PDF File",
                data=pdf_file,
                file_name=pdf_path,
                mime="application/pdf"
            )