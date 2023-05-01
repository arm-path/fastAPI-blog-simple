from fastapi import WebSocket
from sqlalchemy import select

from src.database import async_session_maker
from src.env import SECRET_USER_AUTHENTICATION
from src.user.models import User
from src.user.utils import token_decode


async def get_user_websocket(websocket: WebSocket):
    user_token = websocket.cookies.get('1fastapiusersauth')
    if not user_token:
        return {'status': 500, 'data': [{'error': 'Failed to get cookies'}]}
    answer_decode = token_decode(user_token, SECRET_USER_AUTHENTICATION)
    if answer_decode['status'] != 200:
        return answer_decode
    user_id = answer_decode['token'][0]['sub']
    async with async_session_maker() as session:
        user = await session.execute(select(User).where(User.id == int(user_id)))
    user = user.scalars().one()
    return {'status': 200, 'data': [{'user': user}]}
