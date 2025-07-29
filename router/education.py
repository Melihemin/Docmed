from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
from model import DoctorEducation
from router.auth import get_current_user

router = APIRouter(prefix="/edu", tags=["Education"])
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", response_class=HTMLResponse)
async def vaka(request: Request, db: db_dependency):

    red_count = db.query(DoctorEducation).filter(DoctorEducation.area == "red").count()
    yellow_count = db.query(DoctorEducation).filter(DoctorEducation.area == "yellow").count()
    green_count = db.query(DoctorEducation).filter(DoctorEducation.area == "green").count()
    return templates.TemplateResponse("doctor_vaka.html", {"request": request,"count": db.query(DoctorEducation).count(),
                                        "current_date": datetime.now().strftime('%d %B %Y'),
                                        "red_count": red_count,
                                        "yellow_count": yellow_count,
                                        "green_count": green_count})


@router.post("/", response_class=HTMLResponse)
async def vaka_post(request: Request, db: db_dependency):
    form = await request.form()
    area = form.get("area")
    print("🟡 Gelen form:", area, flush=True)
    disases = db.query(DoctorEducation).filter(
        DoctorEducation.area == area,
    ).all()

    for d in disases:
        print("VAKA:", d.id, d.user_id, d.level, d.area, flush=True)
        print(d.title, d.description, flush=True)

    return templates.TemplateResponse("doctor_vaka.html", 
                                      {"request": request, 
                                       "disases": disases,
                                        "count": db.query(DoctorEducation).count(),
                                        "current_date": datetime.now().strftime('%d %B %Y')})

@router.get("/detail/{vaka_id}", response_class=HTMLResponse)
async def vaka_detail(request: Request, vaka_id: int, db: db_dependency):   
    disase = db.query(DoctorEducation).filter(DoctorEducation.id == vaka_id).first()
    if not disase:
        return "Vaka bulunamadı."
    print("VAKA DETAY:", disase.id, disase.user_id, disase.level, disase.area, disase.description, disase.possibility, disase.medicines, disase.advice, flush=True)
    print(disase.title, disase.description, flush=True)
    return templates.TemplateResponse("edu_detail.html", {"request": request, 
                                                          "disase": disase,
                                                          "current_date": datetime.now().strftime('%d %B %Y'),
                                                          "count": db.query(DoctorEducation).count()})
