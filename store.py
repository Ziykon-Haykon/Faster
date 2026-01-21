from fastapi import FastAPI, Request, Form, APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel
from db.database import SessionLocal, engine
from db.models import User, Cart, CartItem, Order, OrderItem, Product, Base
from sqlalchemy.orm import Session

def add_product(db: Session, title: str, price: float):
    product = Product(title = title, price = price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product