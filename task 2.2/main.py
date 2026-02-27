from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List

app = FastAPI()

class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)

    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str):
        forbidden_words = ['кринж', 'рофл', 'вайб', 'плесень', 'типа', 'короче', 'пон', 'ваще', 'реал']
        v_lower = v.lower()
        for word in forbidden_words:
            if word in v_lower:
                raise ValueError('ЗАПРЕЩЁНКА - ПЕРЕДЕЛЫВАЙ')
        return v

feedbacks: List[Feedback] = []

@app.post("/feedback")
async def create_feedback(feedback: Feedback):
    feedbacks.append(feedback)
    return {"message": f"Спасибо родной, спасибо {feedback.name}! Я тебя услышал и ЗАПОМНИЛ."}

# запуск через /docs