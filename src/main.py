import time

from fastapi import FastAPI
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from src.user.routers import router as user_router
from src.article.routers import router as article_router
from src.tasks.routers import router as task_router

app = FastAPI()


@app.get("/")
@cache(expire=60)
async def index():
    time.sleep(2)
    return {'fastapi': 'Hello Cache!'}


app.include_router(user_router, prefix='/user')
app.include_router(article_router)
app.include_router(task_router)


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi')
