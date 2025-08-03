import streamlit as st
import pandas as pd
import os
from gradecard_generator import generate_pdf
from email_sender import send_email
from logger import log_email_status

st.title("📧 Student Grade Card Generator & Sender")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.dataframe(data)

    if st.button("Generate & Send Grade Cards"):
        output_dir = "gradecards"
        os.makedirs(output_dir, exist_ok=True)
        
        for _, student in data.iterrows():
            try:
                pdf_path = generate_pdf(student, output_dir)
                send_email(
                    receiver=student["Email"],
                    subject="Your Grade Card",
                    body=f"Dear {student['Name']},\n\nPlease find attached your grade card.\n\nRegards,\nSchool Admin",
                    attachment_path=pdf_path
                )
                log_email_status(student["Name"], student["Email"], "Sent")
            except Exception as e:
                log_email_status(student["Name"], student["Email"], f"Failed: {e}")

        st.success("Grade cards generated and emails sent! Check logs for details.")
