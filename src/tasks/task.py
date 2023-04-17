import smtplib
from celery import Celery
from email.message import EmailMessage
from pydantic import EmailStr

from src.env import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

celery = Celery('tasks', broker='redis://127.0.0.1:6379')


def build_message(user_email: EmailStr):
    email = EmailMessage()
    email['Subject'] = 'Subject message'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER
    email.set_content(
        '<div>Hello from fastapi!</div>', subtype='html'
    )
    return email


@celery.task
def send_message(user_email: EmailStr):
    email = build_message(user_email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)