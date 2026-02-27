from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Numbers(BaseModel):
    num1: float
    num2: float

@app.get('/')
async def read_root():
    return {"message": "ЖабиЙ калькулятор 3000 тыщи делай цифры в POST - существо считает."}

@app.post("/calculate")
async def calculate(numbers: Numbers):
    result = numbers.num1 + numbers.num2
    return {"result": result}

# использовал swagger как ui http://127.0.0.1:8000/docs