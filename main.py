from fastapi import FastAPI

from models import users, articles
from schemas import ResponseArticleListSchema, ArticleSchema, ResponseArticleDetail

app = FastAPI()


@app.get('/')
def base():
    return {'title': 'Hello world'}


@app.get('/user/{user_id}')
def get_user(user_id: int):
    user = list(filter(lambda user: user.get('id') == user_id, users))
    return {'status': 200, 'data': user[0]} if user else {'status': 404, 'data': 'page not found'}


@app.get('/user/age/')
def get_user_age(age: int = 18):
    user = list(filter(lambda user: user.get('age') >= age, users))
    return {'status': 200, 'data': user}


@app.post('/user/age/')
def change_user_age(user_id: int, age: int):
    user = list(filter(lambda user: user.get('id') == user_id, users))
    if not user:
        return {'status': 404, 'data': 'page not found'}
    user[0]['age'] = age
    return {'status': 200, 'data': user[0]}


@app.get('/articles/', response_model=ResponseArticleListSchema)
def get_articles():
    return {'status': 200, 'data': articles}


@app.get('/article/{article_id}/')
def get_article(article_id: int):
    article = list(filter(lambda item: item.get('id') == article_id, articles))
    return {'status': 200, 'data': article[0]} if article else {'status': 404, 'data': 'page not found'}


@app.post('/article-create/', response_model=ResponseArticleDetail)
def create_article(article: ArticleSchema):
    return {'status': 200, 'data': article}