from fastapi import APIRouter, Depends

from src.user.routers import current_user
from .task import send_message

router = APIRouter(prefix='/tasks')


@router.get('/send_message')
def send_message_email(user=Depends(current_user)):
    send_message.delay(user.email)
    return{'status': '200'}