from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
from router.auth import get_current_user

router = APIRouter(prefix="/doctor", tags=["doctor"])
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/education", response_class=HTMLResponse)
async def vaka(request: Request):
    return templates.TemplateResponse("doctor_vaka.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("doctor_login.html", {"request": request})


