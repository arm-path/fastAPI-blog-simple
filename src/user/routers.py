from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.user.authentication import auth_backend
from src.user.manager import get_user_manager
from src.user.models import Role
from src.user.models import User
from src.user.schemas import UserRead, UserCreate, RoleCreate
from src.user.utils import token_decode, change_active_user

router = APIRouter(tags=["auth"])

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth"
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt"
)


@router.get('/role/get_roles/')
async def get_roles(session: AsyncSession = Depends(get_async_session)):
    roles = await session.execute(select(Role))
    return {'status': 200, 'roles': roles.scalars().all()}


@router.post('/role/create_role/')
async def create_role(role: RoleCreate, session: AsyncSession = Depends(get_async_session)):
    await session.execute(insert(Role).values(**role.dict()))
    await session.commit()
    return {'status': 200, 'data': ''}


@router.get('/activate/{token}/')
async def activate_user(token: str, session: AsyncSession = Depends(get_async_session)):
    message = token_decode(token)

    if message['status'] == 401:
        raise HTTPException(status_code=401, detail=message)

    user_response = await change_active_user(int(message['token'][0]['id']), session)

    return user_response
