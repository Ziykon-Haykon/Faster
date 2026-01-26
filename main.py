from fastapi import FastAPI, Request, Body, APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel, Field
from typing import Optional
from db.database import SessionLocal, engine
from db.models import User, Cart, CartItem, Order, OrderItem, Product, Base
from store import add_product

class RegisterRequest(BaseModel):
    name: str = Field(default="")
    email: str = Field(default="")
    age: Optional[int] = None
    password: str = Field(default="")

class LoginRequest(BaseModel):
    email: str = Field(default="")
    password: str = Field(default="")

class AddProductRequest(BaseModel):
    title: str = Field(default="")
    price: float = Field(default=0.0)

async def get_data(request: Request) -> dict:
    content_type = request.headers.get('content-type', '')
    if 'application/json' in content_type:
        body = await request.json()
    else:
        body = dict(await request.form())
    # Convert empty strings to appropriate defaults
    for key in body:
        if body[key] == '':
            if key == 'age':
                body[key] = None
            else:
                body[key] = ""
    return body

app = FastAPI()
templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(engine)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
def say_hello(request: Request, data: dict = Depends(get_data)):
    model = RegisterRequest(**data)
    if not model.name or not model.email or not model.password or model.age is None or model.age <= 0:
        message = "All fields are required and age must be positive"
        return templates.TemplateResponse("index.html", {"request": request, "message": message, "show": "register"})
    
    db = SessionLocal()
    user = User(name=model.name, email=model.email, age=model.age or 0, password=model.password)
    db.add(user)
    db.commit()
    db.close()

    message = f"Registered {model.name}. You can now login."

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": message,
            "show": "login"
        }
    )

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, data: dict = Depends(get_data)):
    model = LoginRequest(**data)
    if not model.email or not model.password:
        message = "Email and password are required"
        return templates.TemplateResponse("index.html", {"request": request, "message": message, "show": "login"})
    
    user = user_get_by_email(email=model.email, password=model.password)
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
def add_product_main(request: Request, data: dict = Depends(get_data)):
    model = AddProductRequest(**data)
    if not model.title or model.price <= 0:
        return {"error": "Title and positive price are required"}
    
    db = SessionLocal()
    product = add_product(db=db, title=model.title, price=model.price)
    db.close()
    return {
        "id": product.id,
        "title": product.title,
        "price": product.price
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)