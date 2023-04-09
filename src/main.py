from fastapi import FastAPI

from src.user.routers import router as user_router

app = FastAPI()

app.include_router(user_router, prefix='/user')


@app.get('/')
def base():
    return {'title': 'Hello world'}
