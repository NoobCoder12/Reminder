from app.config.mail_config import HOST, USERNAME, PASSWORD, PORT
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_mail(to: str, subject: str, body: str):
    msg = MIMEMultipart("alternative")
    msg["From"] = USERNAME
    msg['To'] = to
    msg["Subject"] = subject
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    msg.attach(MIMEText(f"<html><body><p>{body}</p></body></html>", "html", 'utf-8'))
    
    with smtplib.SMTP(HOST, PORT) as server:
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, to, msg.as_string())