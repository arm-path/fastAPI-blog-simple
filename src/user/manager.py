from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from src.env import SECRET_USER_MANAGER
from src.user.models import User
from src.user.utils import get_user_db, token_encode


class UserManager(IntegerIDMixin, BaseUserManager[User, id]):
    reset_password_token_secret = SECRET_USER_MANAGER
    verification_token_secret = SECRET_USER_MANAGER

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        token = token_encode(user)
        print(token)
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
