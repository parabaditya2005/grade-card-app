import streamlit as st
import pandas as pd
import os
import zipfile
from io import BytesIO
from gradecard_generator import generate_pdf
from email_sender import send_email

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Grade Card Generator", page_icon="🎓", layout="centered")

# ---- CUSTOM CSS ----
st.markdown("""
    <style>
        body {
            background-color: #f7f7f7;
        }
        .block-container {
            max-width: 900px;
            margin: auto;
            padding-top: 2rem;
        }
        h1, h2, h3, h4 {
            text-align: center;
            color: #1C3652;
            font-family: 'Helvetica', sans-serif;
        }
        .header-logo {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 120px;
        }
        .stButton button {
            background-color: #4E81BD;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
        }
        .stButton button:hover {
            background-color: #365f8c;
            color: white;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .success-box {
            background: #d4edda;
            color: #155724;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
        .error-box {
            background: #f8d7da;
            color: #721c24;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2>🎓 Student Grade Card Generator & Sender</h2>", unsafe_allow_html=True)
st.write("---")

# ---- FILE UPLOAD CARD ----
st.markdown("<div class='card'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload CSV file with student marks", type=["csv"])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Preview Card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("### Preview of Uploaded Data")
    st.dataframe(df)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Generate PDFs ----
    if st.button("Generate Grade Cards"):
        output_dir = "grade_cards"
        os.makedirs(output_dir, exist_ok=True)

        for _, student in df.iterrows():
            generate_pdf(student, output_dir)

        st.markdown("<div class='success-box'>Grade cards generated successfully!</div>", unsafe_allow_html=True)

        # ZIP Download
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for _, student in df.iterrows():
                filename = f"{student['Name'].replace(' ', '_')}_gradecard.pdf"
                filepath = os.path.join(output_dir, filename)
                zipf.write(filepath, arcname=filename)
        zip_buffer.seek(0)

        st.download_button(
            label="📥 Download All Grade Cards (ZIP)",
            data=zip_buffer,
            file_name="grade_cards.zip",
            mime="application/zip"
        )

    # ---- Email Sending ----
    if st.button("Send Grade Cards via Email"):
        output_dir = "grade_cards"
        if not os.path.exists(output_dir):
            st.markdown("<div class='error-box'>Generate grade cards first!</div>", unsafe_allow_html=True)
        else:
            for _, student in df.iterrows():
                pdf_path = os.path.join(output_dir, f"{student['Name'].replace(' ', '_')}_gradecard.pdf")
                try:
                    send_email(
                        receiver=student['Email'],
                        subject="Your Grade Card - XYZ College",
                        body=f"Dear {student['Name']},\n\nPlease find attached your grade card.\n\nRegards,\nXYZ College",
                        attachment_path=pdf_path
                    )
                    st.success(f"Email sent succesfully !!")
                except Exception as e:
                    st.error(f"Failed to send {e}")
