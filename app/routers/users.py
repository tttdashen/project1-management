from datetime import datetime, timedelta, UTC
import hashlib

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import UserCreate, UserOut, Token, Msg

SECRET_KEY = "demo-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

users_router = APIRouter(prefix="/users", tags=["Users"])
public_router = APIRouter(tags=["Auth"])


# -------- utils --------
def _hash(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


def _verify(raw: str, hashed: str) -> bool:
    return _hash(raw) == hashed


# -------- 注册 --------
@users_router.post(
    "",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": Msg}},
)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")

    new_user = models.User(
        username=payload.username,
        password=_hash(payload.password),
        is_admin=(payload.username == "root"),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# -------- 登录核心 --------
def _do_login(form: OAuth2PasswordRequestForm, db: Session) -> Token:
    user = db.query(models.User).filter(models.User.username == form.username).first()
    if not user or not _verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="密码错误")

    exp = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": user.username, "exp": exp}, SECRET_KEY, ALGORITHM)
    return Token(access_token=token)


# /users/login
@users_router.post("/login", response_model=Token, responses={400: {"model": Msg}})
def login_users(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return _do_login(form, db)


# /login
@public_router.post("/login", response_model=Token, responses={400: {"model": Msg}})
def login_root(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return _do_login(form, db)
