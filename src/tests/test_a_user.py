from httpx import AsyncClient
from sqlalchemy import insert, select

from src.tests.conftest import async_sessionmaker_test
from src.user.models import Role, User
from src.user.utils import token_encode


async def test_create_role():
    async with async_sessionmaker_test() as session:
        await session.execute(insert(Role).values(title='user'))
        await session.commit()

        result = await session.execute(select(Role))
        assert result.scalars().one().id == 1, 'Role not added'


async def test_auth_register(async_client: AsyncClient):
    response = await async_client.post(
        '/user/auth/register',
        json={'email': 'user@example.com',
              'password': 'string',
              'role_id': 1,
              'first_name': 'string',
              'last_name': 'string'
              })
    assert response.status_code == 201, 'User not added'
    async with async_sessionmaker_test() as session:
        result = await session.execute(select(User).where(User.email == 'user@example.com'))
        assert result.scalars().one().email == 'user@example.com', 'No users'


async def test_login(async_client: AsyncClient):
    response = await async_client.post(
        '/user/auth/jwt/login',
        headers={'accept': 'application/json'},
        data={'username': 'user@example.com', 'password': 'string', })
    assert response.status_code == 400


async def test_activate_user(async_client: AsyncClient):
    async with async_sessionmaker_test() as session:
        result = await session.execute(select(User).where(User.email == 'user@example.com'))
        user = result.scalars().one()
        token = token_encode(user)
        assert user.is_active == False

    response = await async_client.get(f'/user/activate/{token}/')
    assert response.status_code == 200

    async with async_sessionmaker_test() as session:
        result = await session.execute(select(User).where(User.email == 'user@example.com'))
        assert result.scalars().one().is_active == True


async def test_login_active(async_client: AsyncClient):
    response = await async_client.post(
        '/user/auth/jwt/login',
        headers={'accept': 'application/json'},
        data={'username': 'user@example.com', 'password': 'string', })
    assert response.status_code == 200
    assert async_client.cookies.get('fastapiusersauth') != None
