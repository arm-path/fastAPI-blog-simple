from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from src.database import get_async_session
from src.article.schemas import ArticleCreate
from src.article.models import Article

router = APIRouter(
    prefix="/article",
    tags=["article"]
)


@router.post('/')
async def create_article(article: ArticleCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Article).values(**article.dict())
        await session.execute(stmt)
        await session.commit()
    except IntegrityError as erorrData:
        if erorrData.orig.__cause__.__class__ == UniqueViolationError:
            raise HTTPException(status_code=400, detail={'data': 'title: must be unique'})
        if erorrData.orig.__cause__.__class__ == ForeignKeyViolationError:
            raise HTTPException(status_code=400, detail={'data': 'user_id: is missing from the table'})
        else:
            print('ERR: create_article: ', erorrData)
            raise HTTPException(status_code=500, detail={'data': 'Server error'})

    return {'status': 200, 'data': ''}


@router.get('/')
async def get_articles(session: AsyncSession = Depends(get_async_session)):
    articles = await session.execute(select(Article))
    return {'status': 200, 'articles': articles.scalars().all()}


@router.get('/search/{search}')
async def search_articles(search: str, session: AsyncSession = Depends(get_async_session)):
    articles = await session.execute(select(Article).where(Article.title.like(f'%{search}%')))
    return {'status': 200, 'articles': articles.scalars().all()}
