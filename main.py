from fastapi import FastAPI

app = FastAPI()

users = [
    {'id': 1, 'first_name': 'Bob', 'age': 18},
    {'id': 2, 'first_name': 'Jasica', 'age': 21},
    {'id': 3, 'first_name': 'Alex', 'age': 30},
    {'id': 4, 'first_name': 'Kate', 'age': 16},
    {'id': 5, 'first_name': 'Adam', 'age': 17}
]


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
