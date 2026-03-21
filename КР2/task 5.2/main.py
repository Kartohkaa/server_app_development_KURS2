from fastapi import FastAPI, HTTPException, Cookie, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uuid
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

@app.post("/login")
async def login(login_data: LoginData):
    if login_data.username not in valid_users:
        raise HTTPException(status_code=401, detail="Неверные данные")
    
    if valid_users[login_data.username] != login_data.password:
        raise HTTPException(status_code=401, detail="Неверные данные")
    
    user_id = str(uuid.uuid4())
    
    session_token = serializer.dumps(user_id)
    
    response = JSONResponse(content={"message": "Вход успешен", "user_id": user_id})
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=3600,
        secure=False,
        samesite="lax"
    )
    return response

@app.get("/profile")
async def get_profile(session_token: Optional[str] = Cookie(None)):
    if session_token is None:
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    try:
        user_id = serializer.loads(session_token, max_age=3600)
    except BadSignature:
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    return {
        "user_id": user_id,
        "profile": {
            "name": "User Profile",
            "email": "user@example.com"
        }
    }

@app.post("/logout")
async def logout():
    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie("session_token")
    return response