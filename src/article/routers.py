from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from src.database import get_async_session
from src.article.schemas import ArticleCreate
from src.article.models import Article

router = APIRouter(
    prefix="/article",
    tags=["article"]
)


@router.post('/')
async def create_article(article: ArticleCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Article).values(**article.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 200}


@router.get('/')
async def get_articles(session: AsyncSession = Depends(get_async_session)):
    articles = await session.execute(select(Article))
    return {'status': 200, 'articles': articles.scalars().all()}


@router.get('/search/{search}')
async def search_articles(search: str, session: AsyncSession = Depends(get_async_session)):
    articles = await session.execute(select(Article).where(Article.title.like(f'%{search}%')))
    return {'status': 200, 'articles': articles.scalars().all()}
