from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Feedback(BaseModel):
    name: str
    message: str

feedbacks = []

@app.post("/feedback")
async def create_feedback(feedback: Feedback):
    feedbacks.append(feedback)
    return {"message": f"Услышал тебя родной, жабий чмоки в пупоки. Спасибо, {feedback.name}."}

# запуск через /docs