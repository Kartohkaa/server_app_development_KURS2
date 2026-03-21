from fastapi import FastAPI, HTTPException, Cookie, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Tuple
import uuid
import time
from itsdangerous import URLSafeTimedSerializer, BadSignature

app = FastAPI()

SECRET_KEY = "my-super-secret-key-change-in-production"
serializer = URLSafeTimedSerializer(SECRET_KEY)

valid_users = {
    "user123": "password123"
}

class LoginData(BaseModel):
    username: str
    password: str

def create_token(user_id: str, timestamp: int) -> str:
    data = f"{user_id}.{timestamp}"
    return serializer.dumps(data)

def parse_token(token: str) -> Tuple[Optional[str], Optional[int]]:
    try:
        data = serializer.loads(token)
        user_id, timestamp = data.split('.')
        return user_id, int(timestamp)
    except (BadSignature, ValueError, AttributeError):
        return None, None

@app.post("/login")
async def login(login_data: LoginData):
    if login_data.username not in valid_users:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    
    if valid_users[login_data.username] != login_data.password:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    
    user_id = str(uuid.uuid4())
    current_time = int(time.time())
    session_token = create_token(user_id, current_time)
    
    response = JSONResponse(content={"message": "Вход выполнен успешно"})
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=300,
        secure=False,
        samesite="lax"
    )
    return response

@app.get("/profile")
async def get_profile(response: Response, session_token: Optional[str] = Cookie(None)):
    if session_token is None:
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    user_id, token_time = parse_token(session_token)
    
    if user_id is None or token_time is None:
        raise HTTPException(status_code=401, detail="Недействительная сессия")
    
    current_time = int(time.time())
    time_passed = current_time - token_time
    
    if time_passed >= 300:
        raise HTTPException(status_code=401, detail="Сессия истекла")
    
    if time_passed >= 180:
        new_time = current_time
        new_token = create_token(user_id, new_time)
        response.set_cookie(
            key="session_token",
            value=new_token,
            httponly=True,
            max_age=300,
            secure=False,
            samesite="lax"
        )
    
    return {
        "user_id": user_id,
        "profile": {
            "name": "User Profile",
            "email": "user@example.com"
        }
    }

@app.post("/logout")
async def logout():
    response = JSONResponse(content={"message": "Выход выполнен успешно"})
    response.delete_cookie("session_token")
    return response