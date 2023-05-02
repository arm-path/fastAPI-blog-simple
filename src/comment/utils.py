from fastapi import WebSocket
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.database import async_session_maker
from src.env import SECRET_USER_AUTHENTICATION
from src.user.models import User
from src.user.utils import token_decode
from src.article.models import Article


async def get_user_websocket(websocket: WebSocket):
    user_token = websocket.cookies.get('fastapiusersauth')
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


async def get_article_websocket(id_article):
    try:
        id_article = int(id_article)
    except ValueError:
        return {'status': 500, 'data': [{'error': 'The id_article argument expects a number'}]}
    async with async_session_maker() as session:
        try:
            article = await session.execute(select(Article).where(Article.id == id_article))
            article = article.scalars().one()
        except NoResultFound:
            return {'status': 500, 'data': [{'error': 'The request returned an empty result'}]}
        return {'status': 200, 'data': [{'article': article}]}
