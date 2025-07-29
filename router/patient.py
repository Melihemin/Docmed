from typing import Annotated
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from model import DoctorEducation, User
import sys
import os
from router.auth import SECRET_KEY, get_db, redirect_to_login
from jose import jwt, JWTError
from router.auth import get_current_user
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter(prefix="/patient", tags=["Patient"])
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# Patient list
@router.get("/list", response_class=HTMLResponse)
async def patient_list(request: Request, db: db_dependency, user: user_dependency):
    if not user:
        
        return RedirectResponse(url="/auth/login", status_code=302)

    Users = db.query(User).all()
    users_area = db.query(DoctorEducation).filter(DoctorEducation.user_id == user["id_number"]).all()


    return templates.TemplateResponse("patients.html", {"request": request,
                                                        "Users" : Users, 
                                                        "users_area":users_area})


@router.get("/detail/{id_number}", response_class=HTMLResponse)
async def patient_detail(request: Request, id_number: str, db: db_dependency, user: user_dependency):
    token = request.cookies.get("access_token")
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if payload.get("id_number") and payload.get("name"):
                patient = db.query(User).filter(User.id_number == id_number).first()
                info = db.query(DoctorEducation).filter(DoctorEducation.user_id == id_number).first()
                if not patient:
                     return RedirectResponse(url="/auth/login", status_code=302)

            return templates.TemplateResponse("doctor_patient.html", {
                "request": request,
                "user": patient,
                "info": info
            })
            
            
        except JWTError:
            response = RedirectResponse(url="/auth/login", status_code=302)
            response.delete_cookie("access_token", path="/")


@router.get("/report/{id_number}", response_class=HTMLResponse)
async def report(request: Request, id_number: str, db: db_dependency, user: user_dependency):
    token = request.cookies.get("access_token")
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if payload.get("id_number") and payload.get("name"):
                patient = db.query(User).filter(User.id_number == id_number).first()
                info = db.query(DoctorEducation).filter(DoctorEducation.user_id == id_number).first()
                if not patient:
                     return RedirectResponse(url="/auth/login", status_code=302)

            return templates.TemplateResponse("reports.html", {
                "request": request,
                "user": patient,
                "info": info
            })
            
            
        except JWTError:
            response = RedirectResponse(url="/auth/login", status_code=302)
            response.delete_cookie("access_token", path="/")

