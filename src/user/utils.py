from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi_users.db import SQLAlchemyUserDatabase
from jwt.exceptions import ExpiredSignatureError
from sqlalchemy import update
from sqlalchemy.exc import NoResultFound
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


def token_decode(token, secret):
    try:
        token = jwt.decode(token, secret, algorithms="HS256")
        answer_decode = {'status': 200, 'token': [token, ]}
    except ExpiredSignatureError:
        answer_decode = {'status': 401, 'message': 'Token expired.'}
    except Exception as e:
        answer_decode = {'status': 401, 'message': 'Invalid token.'}
    return answer_decode


async def change_active_user(user_id, session: AsyncSession):
    try:
        update_stmt = (
            update(User)
                .where(User.id == user_id)
                .values(is_active=True)
                .returning(User)
        )

        result = await session.execute(update_stmt)
        await session.commit()
        user = result.scalars().one()
    except NoResultFound:
        raise HTTPException(status_code=500,
                            detail={'status': 500, 'message': 'A database result was required but none was found.'})
    except Exception as e:
        raise HTTPException(status_code=500, detail={'status': 500, 'message': 'Server error.'})

    user_response = {
        'email': user.email,
        'first_name': user.first_name, 'last_name': user.last_name,
        'is_active': user.is_active
    }
    return user_response
