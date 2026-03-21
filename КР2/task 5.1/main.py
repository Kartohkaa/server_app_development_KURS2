from fastapi import FastAPI, HTTPException, Cookie, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()

valid_users = {
    "user123": "password123"
}

sessions = {}

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(login_data: LoginData):
    if login_data.username not in valid_users:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    
    if valid_users[login_data.username] != login_data.password:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    
    session_token = str(uuid.uuid4())
    sessions[session_token] = login_data.username
    
    response = JSONResponse(content={"message": "Логин успешен"})
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return response

@app.get("/user")
async def get_user(session_token: Optional[str] = Cookie(None)):
    if session_token is None:
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    if session_token not in sessions:
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    username = sessions[session_token]
    
    return {
        "username": username,
        "profile": {
            "name": "User Profile",
            "email": f"{username}@example.com"
        }
    }

@app.post("/logout")
async def logout(session_token: Optional[str] = Cookie(None)):
    if session_token and session_token in sessions:
        del sessions[session_token]
    
    response = JSONResponse(content={"message": "Выход успешен"})
    response.delete_cookie("session_token")
    return response

@app.get('/')
async def root():
    return {"message": "мяу-сервер активирован. Шлёпай в /docs"}
