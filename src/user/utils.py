import jwt
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.env import SECRET_EMAIL_CONFIRMATION
from src.user.models import User


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


def token_encode(user):
    token = jwt.encode({
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }, SECRET_EMAIL_CONFIRMATION, algorithm='HS256')

    return token


def token_decode(token):
    token = jwt.decode(token, SECRET_EMAIL_CONFIRMATION, algorithms="HS256")
    return token
