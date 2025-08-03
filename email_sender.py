import smtplib
from email.message import EmailMessage
import ssl

def send_email(receiver, subject, body, attachment_path):
    sender = "parabaditya2005@gmail.com"
    password = "hzvf ffsj kbqp gpnw"  # Use Gmail App Password

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=f.name.split("/")[-1])

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
