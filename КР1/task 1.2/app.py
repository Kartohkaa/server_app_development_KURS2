from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)