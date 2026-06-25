import smtplib
from email.mime.text import MIMEText
from config import EMAIL_USER, EMAIL_PASS, EMAIL_RECEIVERS

def send_email(subject, content):
    msg = MIMEText(content, "html", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = ",".join(EMAIL_RECEIVERS)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, EMAIL_RECEIVERS, msg.as_string())
    server.quit()
