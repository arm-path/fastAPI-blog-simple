from fastapi import FastAPI

from src.user.routers import router as user_router
from src.article.routers import router as article_router

app = FastAPI()

app.include_router(user_router, prefix='/user')
app.include_router(article_router)
