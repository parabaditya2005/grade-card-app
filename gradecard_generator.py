from fpdf import FPDF
import os
from datetime import datetime

# Colors
COLOR_NAVY = (28, 54, 82)
COLOR_BLUE = (78, 129, 189)
COLOR_LIGHT_GRAY = (240, 240, 240)
COLOR_WHITE = (255, 255, 255)
COLOR_DARK_TEXT = (50, 50, 50)

def calculate_grade(percentage):
    if percentage >= 90: return 'A+'
    elif percentage >= 80: return 'A'
    elif percentage >= 70: return 'B'
    elif percentage >= 60: return 'C'
    elif percentage >= 50: return 'D'
    else: return 'F'

def generate_pdf(student, output_path):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()

    # Border
    pdf.set_draw_color(*COLOR_NAVY)
    pdf.set_line_width(0.5)
    pdf.rect(10, 10, 190, 277)

    # Banner
    pdf.set_fill_color(*COLOR_NAVY)
    pdf.rect(10, 10, 190, 40, 'F')

    # Logo
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 15, 15, 25)

    # College name & title
    pdf.set_text_color(*COLOR_WHITE)
    pdf.set_font("Helvetica", 'B', 22)
    pdf.set_xy(0, 20)
    pdf.cell(210, 10, "XYZ College of Science", align='C')

    pdf.set_font("Helvetica", 'I', 13)
    pdf.set_xy(0, 30)
    pdf.cell(210, 10, "Final Year B.Sc. (Computer Science) - Grade Card", align='C')
    pdf.set_text_color(*COLOR_DARK_TEXT)

    # Student Info
    pdf.set_font("Times", '', 12)
    pdf.set_xy(20, 60)
    pdf.cell(95, 8, f"Name: {student['Name']}")
    pdf.cell(95, 8, f"Roll No: {student['RollNo']}", ln=1)

    pdf.set_xy(20, 68)
    pdf.cell(95, 8, f"Course: {student['Course']}")
    pdf.cell(95, 8, f"Semester: {student['Semester']}", ln=1)

    pdf.set_xy(20, 76)
    pdf.cell(95, 8, f"Email: {student['Email']}", ln=1)

    # Divider
    pdf.set_draw_color(200, 200, 200)
    pdf.line(20, 84, 190, 84)

    # Table Header
    pdf.set_xy(20, 90)
    pdf.set_fill_color(*COLOR_BLUE)
    pdf.set_text_color(*COLOR_WHITE)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(50, 12, "Subject", 1, 0, 'C', True)
    pdf.cell(30, 12, "Unit Test", 1, 0, 'C', True)
    pdf.cell(30, 12, "Practical", 1, 0, 'C', True)
    pdf.cell(30, 12, "Final Exam", 1, 0, 'C', True)
    pdf.cell(30, 12, "Total", 1, 1, 'C', True)

    # Subject Rows
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Times", '', 12)
    subjects = ["AI", "IoT", "CF", "STQA", "Project"]
    total_sum = 0
    max_marks = 0
    y_position = 102

    for i, sub in enumerate(subjects):
        pdf.set_fill_color(*COLOR_LIGHT_GRAY if i % 2 == 0 else COLOR_WHITE)
        ut = student[f"{sub}_UT"]
        pr = student[f"{sub}_Practical"]
        fe = student[f"{sub}_Final"]
        total = ut + pr + fe
        total_sum += total
        max_marks += 150

        pdf.set_xy(20, y_position)
        pdf.cell(50, 12, sub, 1, 0, 'L', True)
        pdf.cell(30, 12, str(ut), 1, 0, 'C', True)
        pdf.cell(30, 12, str(pr), 1, 0, 'C', True)
        pdf.cell(30, 12, str(fe), 1, 0, 'C', True)
        pdf.cell(30, 12, str(total), 1, 1, 'C', True)
        y_position += 12

    # Summary Boxes
    percentage = (total_sum / max_marks) * 100
    cgpa = round(percentage / 10, 2)
    grade = calculate_grade(percentage)

    summary_y = y_position + 12
    pdf.set_xy(30, summary_y)
    pdf.set_font("Helvetica", 'B', 10)
    pdf.set_text_color(*COLOR_DARK_TEXT)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(45, 8, "Percentage", 1, 0, 'C', True)
    pdf.set_x(82.5)
    pdf.cell(45, 8, "CGPA", 1, 0, 'C', True)
    pdf.set_x(135)
    pdf.set_fill_color(*COLOR_NAVY)
    pdf.set_text_color(*COLOR_WHITE)
    pdf.cell(45, 8, "Overall Grade", 1, 1, 'C', True)

    pdf.set_xy(30, summary_y + 8)
    pdf.set_font("Times", 'B', 16)
    pdf.set_text_color(*COLOR_DARK_TEXT)
    pdf.set_fill_color(*COLOR_WHITE)
    pdf.cell(45, 15, f"{percentage:.2f}%", 1, 0, 'C', True)
    pdf.set_x(82.5)
    pdf.cell(45, 15, f"{cgpa:.2f}", 1, 0, 'C', True)
    pdf.set_x(135)
    pdf.set_fill_color(*COLOR_BLUE)
    pdf.set_text_color(*COLOR_WHITE)
    pdf.cell(45, 15, grade, 1, 1, 'C', True)

    # --- Signatures at Bottom Left & Right ---
    sig_y = max(summary_y + 50, 250)
    if sig_y > 270:
        sig_y = 270

    # HOD Signature Image
    if os.path.exists("hod_sign.png"):
        pdf.image("hod_sign.png", 25, sig_y - 15, 40)

    # Principal Signature Image
    if os.path.exists("principal_sign.png"):
        pdf.image("principal_sign.png", 125, sig_y - 15, 40)

    # HOD Line + Label
    pdf.set_font("Helvetica", '', 12)
    pdf.set_text_color(*COLOR_DARK_TEXT)
    pdf.set_xy(20, sig_y)
    pdf.cell(70, 0, "____________________________", 0, 0, 'C')
    pdf.set_xy(20, sig_y + 8)
    pdf.set_font("Helvetica", 'I', 11)
    pdf.cell(70, 8, "Head of Department", 0, 0, 'C')

    # Principal Line + Label
    pdf.set_font("Helvetica", '', 12)
    pdf.set_xy(120, sig_y)
    pdf.cell(70, 0, "____________________________", 0, 0, 'C')
    pdf.set_xy(120, sig_y + 8)
    pdf.set_font("Helvetica", 'I', 11)
    pdf.cell(70, 8, "Principal", 0, 0, 'C')

    # Date below Principal
    date_str = datetime.now().strftime("%d-%m-%Y")
    pdf.set_xy(120, sig_y + 18)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(70, 8, f"Issue Date: {date_str}", 0, 0, 'C')

    # Save PDF
    filename = os.path.join(output_path, f"{student['Name'].replace(' ', '_')}_gradecard.pdf")
    pdf.output(filename)
    return filename
