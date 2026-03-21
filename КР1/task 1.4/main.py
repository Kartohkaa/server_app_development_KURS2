from fastapi import FastAPI
from models import User

app = FastAPI()

current_user = User(
    name = "Шульга Михаил",
    id = 30
)

@app.get('/users')
async def get_user():
    return current_user

@app.get('/')
async def root():
    return {"message": "Жабий-сервер работает."}

# чтобы посмотреть данные юзера надо перейти на http://127.0.0.1:8001/users, то-есть /users