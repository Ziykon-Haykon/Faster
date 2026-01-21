from fastapi import FastAPI, Request, Form, APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel
from db.database import SessionLocal, engine
from db.models import User, Cart, CartItem, Order, OrderItem, Product, Base
from store import add_product

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
    db.close()

    message = f"Registered {name}. You can now login."

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": message,
            "show": "login"
        }
    )

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = user_get_by_email(email=email, password=password)
    if not user:
        message = "Invalid email or password"
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "message": message,
                "show": "login"
            }
        )
    message = f"Welcome back, {user.name}!"
    return templates.TemplateResponse(
        "hello.html",
        {
            "request": request,
            "message": message,
            "show": "none"
        }
    )

def user_get_by_email(email: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email,User.password == password).first()
    if not user:
        return 
    else:
        return user

@app.post("/addProduct")
def add_product_main(request: Request, title: str = Form(...), price: float = Form(...)):
    db = SessionLocal()
    product = add_product(db=db, title=title, price=price)
    db.close()
    return {
        "id": product.id,
        "title": product.title,
        "price": product.price
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)