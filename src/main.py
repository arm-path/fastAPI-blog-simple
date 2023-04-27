import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi.staticfiles import StaticFiles

from src.user.routers import router as user_router
from src.article.routers import router as article_router
from src.sample_pages.routers import router as page_router

app = FastAPI()
app.mount('/static', StaticFiles(directory='src/static/'), name='static')


@app.get("/")
@cache(expire=60)
async def index():
    time.sleep(2)
    return {'fastapi': 'Hello Cache!'}


app.include_router(user_router, prefix='/user')
app.include_router(page_router, prefix='/page')
app.include_router(article_router)

origins = [
    'http://localhost',
    'http://localhost:3030'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi')
