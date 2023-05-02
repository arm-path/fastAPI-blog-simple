from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates

from src.article.routers import get_articles, get_article, search_articles
from src.user.models import User
from src.user.routers import current_active_user

template = Jinja2Templates(directory="src/templates/")

router = APIRouter()


@router.get('/articles/', tags=['sample pages'])
def get_list_article(request: Request, articles=Depends(get_articles)):
    return template.TemplateResponse('article_list.html', {'request': request, 'articles': articles['articles']})


@router.get('/article/{id}', tags=['sample pages'])
def get_detail_article(request: Request, article=Depends(get_article)):
    return template.TemplateResponse('article_detail.html', {'request': request, 'article': article['article']})


@router.get('/articles/{search}', tags=['sample pages'])
def get_search_article(request: Request, articles=Depends(search_articles)):
    return template.TemplateResponse('article_list.html', {'request': request, 'articles': articles['articles']})
