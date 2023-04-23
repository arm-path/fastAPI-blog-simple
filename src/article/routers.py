from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from src.database import get_async_session
from src.article.schemas import ArticleCreate
from src.article.models import Article
from src.user.models import User
from src.user.routers import current_active_user

router = APIRouter(
    prefix="/article",
    tags=["article"]
)


@router.post('/')
async def create_article(article: ArticleCreate, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    try:
        article = article.dict()
        article['user_id'] = user.id
        article = await session.execute(insert(Article).values(**article).returning(Article))
        await session.commit()
    except IntegrityError as erorrData:
        if erorrData.orig.__cause__.__class__ == UniqueViolationError:
            raise HTTPException(status_code=400, detail={'data': 'title: must be unique'})
        if erorrData.orig.__cause__.__class__ == ForeignKeyViolationError:
            raise HTTPException(status_code=400, detail={'data': 'user_id: is missing from the table'})
        else:
            print('ERR: create_article: ', erorrData)
            raise HTTPException(status_code=500, detail={'data': 'Server error'})

    return {'status': 200, 'article': article.scalars().one()}


@router.get('/get/{id}')
async def get_article(id: int, session: AsyncSession = Depends(get_async_session)):
    article = await session.execute(select(Article).where(Article.id == id))
    try:
        article = article.scalars().one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail={'status': 404, 'article': []})
    return {'status': 200, 'article': article}


@router.get('/')
async def get_articles(session: AsyncSession = Depends(get_async_session)):
    articles = await session.execute(select(Article))
    return {'status': 200, 'articles': articles.scalars().all()}


@router.get('/search/{search}')
async def search_articles(search: str, session: AsyncSession = Depends(get_async_session)):
    articles = await session.execute(select(Article).where(Article.title.like(f'%{search}%')))
    return {'status': 200, 'articles': articles.scalars().all()}
