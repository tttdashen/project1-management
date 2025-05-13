from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/users", tags=["users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- 注册 ----------
@router.post(
    "", 
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED   # ✅ 设定 201
)   # ← 返回码保持 200，符合测试
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")  # 和测试信息一致

    hashed_pw = pwd_context.hash(user_in.password)
    user = models.User(username=user_in.username, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ---------- 登录 ----------
@router.post("/login", response_model=schemas.Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),   # 参数名统一
    db: Session = Depends(get_db)
):
    # 1. 查询用户
    user = (db.query(models.User)
              .filter(models.User.username == form_data.username)
              .first())
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在")

    # 2. 验证密码
    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="密码错误")

    # 3. 生成 JWT
    token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
