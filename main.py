from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/hello", response_class=HTMLResponse)
def say_hello(name: str = Form(...), age: int = Form(...)):
    return f"<h2>Hi, {name}, your age is {age}!<h2>"