from fastapi import FastAPI

application = FastAPI()

@application.get("/")
async def root():
    return {"message": "ЙОоооООУУ"}

  # return {"message": "авторелоад: пельмешки жабьи работают?"}