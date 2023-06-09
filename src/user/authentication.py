from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy

from src.env import SECRET_USER_AUTHENTICATION

SECRET = SECRET_USER_AUTHENTICATION

cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600, token_audience=None)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
