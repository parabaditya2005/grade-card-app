import streamlit as st
import pandas as pd
import os
import zipfile
from io import BytesIO
from gradecard_generator import generate_pdf
from email_sender import send_email

# --- Streamlit Page Config ---
st.set_page_config(page_title="Grade Card Generator", page_icon="🎓", layout="centered")

# --- App Title ---
st.markdown(
    """
    <h2 style='text-align:center; color:#1C3652;'>XYZ College of Science</h2>
    <h4 style='text-align:center; color:#4E81BD;'>Final Year B.Sc. (CS) Grade Card Generator</h4>
    """,
    unsafe_allow_html=True
)

st.write("Upload a **CSV file** with student data to generate and send grade cards.")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Preview of Uploaded Data")
    st.dataframe(df)

    # --- Generate Grade Cards ---
    if st.button("Generate Grade Cards"):
        output_dir = "grade_cards"
        os.makedirs(output_dir, exist_ok=True)

        for _, student in df.iterrows():
            generate_pdf(student, output_dir)

        st.success("Grade cards generated successfully!")

        # --- Offer ZIP Download ---
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

        # Individual Downloads
        st.write("### Download Individual Grade Cards")
        for _, student in df.iterrows():
            file_path = os.path.join(output_dir, f"{student['Name'].replace(' ', '_')}_gradecard.pdf")
            with open(file_path, "rb") as file:
                st.download_button(
                    label=f"Download {student['Name']}'s Grade Card",
                    data=file,
                    file_name=f"{student['Name']}_gradecard.pdf",
                    mime="application/pdf"
                )

    # --- Send Emails ---
    if st.button("Send Grade Cards via Email"):
        output_dir = "grade_cards"
        if not os.path.exists(output_dir):
            st.error("Please generate grade cards first!")
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
                    st.success(f"Email sent to {student['Name']} ({student['Email']})")
                except Exception as e:
                    st.error(f"Failed to send email to {student['Name']} ({student['Email']}): {e}")
