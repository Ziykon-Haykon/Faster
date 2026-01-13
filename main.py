from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/hello", response_class=HTMLResponse)
def say_hello(request: Request, name: str = Form(...), age: int = Form(...)):

    message = f"Привет, {name}, возраст {age}"

    if age > 120:
        message = "либо очень старый, либо возраст нетот"

    return templates.TemplateResponse(
        "hello.html",
        {
            "request": request,
            "message": message
        }
    )

@app.post("/age", response_class=HTMLResponse)
def change_age(request: Request, age: int = Form(...), name: str = Form(...)):
    message = f"Привет, {name}, возраст {age}"
    return templates.TemplateResponse(
        "hello.html",
        {
            "request": request,
            "message": message
        }
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)