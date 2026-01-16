from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel
from db.database import SessionLocal, engine
from db.models import User, Base

app = FastAPI()
templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(engine)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
def say_hello(request: Request, name: str = Form(...), email: str = Form(...), age: int = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = User(name = name, email=email, age = age, password = password)
    db.add(user)
    db.commit()
    db.close

    message = f"name is {name}, age is {age}, password is {password}"

    return templates.TemplateResponse(
        "hello.html",
        {
            "request": request,
            "message": message
        }
    )

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = user_get_by_email(email=email, password=password)
    message = f"name is {user.name}, age is {user.age}, password is {password}"
    return templates.TemplateResponse(
        "hello.html",
        {
            "request": request,
            "message": message
        }
    )

def user_get_by_email(email: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email, User.password == password).first()
    db.close()
    return user

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)