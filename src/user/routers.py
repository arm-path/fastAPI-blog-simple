from fastapi import APIRouter

from fastapi_users import FastAPIUsers

from src.user.models import User
from src.user.manager import get_user_manager
from src.user.authentication import auth_backend
from src.user.schemas import UserRead, UserCreate

router = APIRouter(tags=["auth"])

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth"
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt"
)