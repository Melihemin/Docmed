# server.py
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from database import Base, engine
from router import patient, doctor, auth, education
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from router.auth import get_db, redirect_to_login, SECRET_KEY, get_token_from_request
from jose import jwt, JWTError
import logging
import os
from router.patient import user_dependency
from model import DoctorEducation
from pathlib import Path
from urllib.parse import quote
from gemini_model import get_medicine_suggestion, get_doctor_advice, get_possible_diseases, get_title, get_description, get_level, get_area




# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app oluştur
app = FastAPI(
    title="Hastane Randevu Sistemi",
    description="Hasta ve doktor randevu yönetim sistemi",
    version="1.0.0",
    docs_url="/docs" if os.getenv("DEBUG", "False").lower() == "true" else None,
    redoc_url="/redoc" if os.getenv("DEBUG", "False").lower() == "true" else None
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Güvenlik middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.localhost"]
)

# Templates konfigürasyonu
templates = Jinja2Templates(directory="templates")
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Veritabanı tablolarını oluştur
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Veritabanı tabloları başarıyla oluşturuldu")
except Exception as e:
    logger.error(f"Veritabanı oluşturma hatası: {e}")

# Static files mount (hata handling ile)
static_path = Path("static")
if static_path.exists() and static_path.is_dir():
    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")
        logger.info("Static dosyalar başarıyla mount edildi")
    except Exception as e:
        logger.error(f"Static dosya mount hatası: {e}")
else:
    logger.warning("Static klasörü bulunamadı")

# Router'ları ekle
app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(education.router)

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/home")
async def homepage(request: Request):
    return templates.TemplateResponse("docmed-master/index.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    token = request.cookies.get("access_token")
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if payload.get("id_number") and payload.get("name"):
                return RedirectResponse(url="/index", status_code=302)
        except JWTError:
            response = RedirectResponse(url="/auth/login", status_code=302)
            response.delete_cookie("access_token", path="/")
            return response
    return RedirectResponse(url="/auth/login", status_code=302)

@app.get("/index", response_class=HTMLResponse)
async def home(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        logger.warning("Index sayfasına token olmadan erişim denemesi")
        return redirect_to_login()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = {
            "id_number": payload.get("id_number"),
            "name": payload.get("name"),
            "surname": payload.get("surname")
        }
        return templates.TemplateResponse("index.html", {"request": request, "user": user})
    except JWTError as e:
        logger.error(f"Token doğrulama hatası: {e}")
        return redirect_to_login()
    except Exception as e:
        logger.error(f"Index sayfası hatası: {e}")
        return redirect_to_login()

@app.post("/index", response_class=HTMLResponse)
async def handle_message(request: Request, db: db_dependency, user: user_dependency):
    form = await request.form()
    message = form.get("message", "").strip()

    title = get_title(message)
    description = get_description(message)
    medicines = get_medicine_suggestion(message)
    doctor_advice = get_doctor_advice(message)
    possible_diseases = get_possible_diseases(message)
    level = get_level(message)
    area = get_area(message)

    db.add(DoctorEducation(
        user_id=user["id_number"],
        title=title,
        description=description,
        medicines=medicines,
        advice=doctor_advice,
        possibility=possible_diseases,
        level=level,
        area=area
    ))

    db.commit()

    return RedirectResponse("/patient/list", status_code=302)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
