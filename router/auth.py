# auth.py
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from starlette import status
from fastapi.templating import Jinja2Templates
from database import SessionLocal
from model import User
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
import secrets
import hashlib

router = APIRouter(prefix="/auth", tags=["Authentication"])
templates = Jinja2Templates(directory="templates")

# TOKEN AYARLARI - Üretim ortamında environment variable kullanın
SECRET_KEY = "acoztm3revp1vfj7ld5sz2ndg5xp79r9fnr2p4hx2dy63h6a8efhj6rm54u8evh8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def get_db():
    """Veritabanı session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)

def get_token_from_request(request: Request, token: Annotated[Optional[str], Depends(oauth2_bearer)] = None):
    """Token'ı cookie'den veya Authorization header'dan al"""
    if token:
        return token
    return request.cookies.get("access_token")

async def get_current_user(request: Request, token: Annotated[Optional[str], Depends(oauth2_bearer)] = None):
    """Mevcut kullanıcıyı token'dan al ve doğrula"""
    access_token = get_token_from_request(request, token)
    
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token bulunamadı",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        id_number: str = payload.get("id_number")
        name: str = payload.get("name")
        surname: str = payload.get("surname")
        exp: int = payload.get("exp")

        # Token süresi kontrol
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token süresi dolmuş"
            )

        if not id_number or not name:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Geçersiz token"
            )

        return {
            "id_number": id_number,
            "name": name,
            "surname": surname
        }

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token doğrulanamadı",
            headers={"WWW-Authenticate": "Bearer"}
        )

user_dependency = Annotated[dict, Depends(get_current_user)]

class Token(BaseModel):
    access_token: str
    token_type: str

class CreateUserRequest(BaseModel):
    id_number: str
    name: str
    surname: str

    
    class Config:
        str_strip_whitespace = True

class LoginRequest(BaseModel):
    id_number: str
    
    class Config:
        str_strip_whitespace = True

def redirect_to_login():
    """Login sayfasına yönlendirme ve cookie temizleme"""
    redirect_response = RedirectResponse(
        url="/auth/login", 
        status_code=status.HTTP_302_FOUND
    )
    redirect_response.delete_cookie("access_token", path="/", domain=None)
    return redirect_response

def create_access_token(id_number: str, name: str, surname: str, expires_delta: Optional[timedelta] = None):
    """JWT token oluştur"""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "id_number": id_number,
        "name": name,
        "surname": surname,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(id_number: str, db: Session):
    """Kullanıcı doğrulama"""
    if not id_number or len(id_number.strip()) != 11:
        return None
    
    return db.query(User).filter(User.id_number == id_number.strip()).first()

def validate_tc_number(tc_number: str) -> bool:
    """TC kimlik numarası doğrulaması"""
    if not tc_number or len(tc_number) != 11 or not tc_number.isdigit():
        return False
    
    # İlk rakam 0 olamaz
    if tc_number[0] == '0':
        return False
    
    # Basit algoritma kontrolü
    try:
        digits = [int(d) for d in tc_number]
        sum_first_10 = sum(digits[:10])
        return sum_first_10 % 10 == digits[10]
    except:
        return False

@router.get("/login")
async def render_login_page(request: Request):
    """Login sayfasını render et"""
    # Eğer zaten giriş yapmışsa index'e yönlendir
    token = request.cookies.get("access_token")
    if token:
        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return RedirectResponse(url="/index", status_code=status.HTTP_302_FOUND)
        except JWTError:
            pass  # Token geçersiz, login sayfasını göster
    
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register")
async def render_register_page(request: Request):
    """Kayıt sayfasını render et"""
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    """Yeni kullanıcı kaydet"""
    # TC kimlik numarası doğrulama
    if not validate_tc_number(create_user_request.id_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Geçerli bir TC kimlik numarası giriniz."
        )
    
    # Mevcut kullanıcı kontrolü
    existing_user = db.query(User).filter(
        User.id_number == create_user_request.id_number
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Bu kimlik numarası zaten kayıtlı."
        )

    # İsim ve soyisim kontrolü
    if not create_user_request.name.strip() or not create_user_request.surname.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="İsim ve soyisim boş bırakılamaz."
        )

    try:
        user = User(
            id_number=create_user_request.id_number,
            name=create_user_request.name.strip().title(),
            surname=create_user_request.surname.strip().title(),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {"message": "Kayıt başarıyla tamamlandı."}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Kayıt işlemi sırasında bir hata oluştu."
        )

@router.post("/token")
async def login_for_access_token(login: LoginRequest, db: db_dependency):
    """Login işlemi ve token oluşturma"""
    # TC kimlik numarası doğrulama
    if not validate_tc_number(login.id_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Geçerli bir TC kimlik numarası giriniz."
        )
    
    user = authenticate_user(login.id_number, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kimlik numarası bulunamadı"
        )

    try:
        token = create_access_token(
            id_number=user.id_number,
            name=user.name,
            surname=user.surname,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        # Cookie ile birlikte index sayfasına yönlendir
        response = RedirectResponse(
            url="/index", 
            status_code=status.HTTP_302_FOUND
        )
        response.set_cookie(
            key="access_token",
            value=token,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=False,  # Development için False, production'da True olmalı
            samesite="lax",
            path="/"
        )
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Giriş işlemi sırasında bir hata oluştu."
        )

@router.get("/logout")
async def logout():
    """Çıkış işlemi"""
    return redirect_to_login()

@router.get("/verify")
async def verify_token(user: user_dependency):
    """Token doğrulama endpoint'i"""
    return {"message": "Token geçerli", "user": user}