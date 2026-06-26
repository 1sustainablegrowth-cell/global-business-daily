import smtplib
import socket
from email.mime.text import MIMEText
from config import EMAIL_USER, EMAIL_PASS, EMAIL_RECEIVERS

def send_email(subject, content):
    print("开始连接 Gmail SMTP...")

    msg = MIMEText(content, "html", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = ",".join(EMAIL_RECEIVERS)

    try:
        # 设置连接超时
        socket.setdefaulttimeout(30)

        server = smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
            timeout=30
        )

        print("SMTP连接成功")

        server.login(EMAIL_USER, EMAIL_PASS)
        print("SMTP登录成功")

        server.sendmail(
            EMAIL_USER,
            EMAIL_RECEIVERS,
            msg.as_string()
        )

        print("邮件发送成功")

        server.quit()

    except Exception as e:
        print("邮件发送失败：")
        print(e)
        raise
