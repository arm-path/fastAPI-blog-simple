import smtplib
from email.message import EmailMessage
from pydantic import EmailStr
from celery import Celery

from src.env import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

celery = Celery('tasks', broker='redis://127.0.0.1:6379')


def build_message(user_email: EmailStr, token: str):
    message = EmailMessage()
    message['Subject'] = 'Activation'
    message['From'] = SMTP_USER
    message['To'] = SMTP_USER  # TODO: change user_email.
    message.set_content(
        f"Follow the link to activate your account: <a href='http://127.0.0.1:8000/user/activate/{token}'>Go</a>",
        subtype="html"
    )

    return message


@celery.task
def send_massage(user_email, token):
    email = build_message(user_email, token)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
