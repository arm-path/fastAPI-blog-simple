from httpx import AsyncClient
from sqlalchemy import select, insert

from src.tests.conftest import async_sessionmaker_test
from src.article.models import Article


async def test_create_article_sql():
    async with async_sessionmaker_test() as session:
        stmt = insert(Article).values(title='string', conten='string', user_id=1).returning(Article)
        result_create_article = await session.execute(stmt)
        await session.commit()
        result_get_article = await session.execute(select(Article).where(Article.id == 1))
        assert result_create_article.scalars().one().id == result_get_article.scalars().one().id


async def test_get_articles(async_client: AsyncClient):
    response = await async_client.get('/article/')
    assert response.status_code == 200
    assert len(response.json()['articles']) == 1


async def test_get_article(async_client: AsyncClient):
    response = await async_client.get(f'/article/get/{1}')
    assert response.status_code == 200
    response = await async_client.get(f'/article/get/{2}')
    assert response.status_code == 404


async def test_search_article(async_client: AsyncClient):
    response = await async_client.get('/article/search/st')
    assert len(response.json()['articles']) == 1
    response = await async_client.get('/article/search/what')
    assert len(response.json()['articles']) == 0


async def test_create_article(async_client: AsyncClient):
    response = await async_client.post(
        '/article/',
        json={
            "title": "string3",
            "conten": "string"
        })

    print('------>', response.status_code)
