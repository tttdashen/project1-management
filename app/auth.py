from datetime import datetime, timedelta, UTC

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
# ➕ 改为 HTTPBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.database import get_db
from app import models
from app.schemas import Token, Msg

SECRET_KEY = "demo-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(tags=["Auth"])

# -------------------- 登录接口（保持不变） --------------------
@router.post("/login", response_model=Token, responses={400: {"model": Msg}})
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db:   Session                  = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == form.username).first()
    if not user or not bcrypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="密码错误")

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, ALGORITHM)
    return Token(access_token=token)

# -------------------- Bearer 鉴权方案 --------------------
# auto_error=True ➜ 缺头/格式错立即 403 → FastAPI 转 401
token_scheme = HTTPBearer(auto_error=True)                         # ➕

def get_current_user(
    token_creds: HTTPAuthorizationCredentials = Depends(token_scheme),   # ➕
    db: Session = Depends(get_db),
) -> models.User | None:
    token = token_creds.credentials                                      # ➕
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise cred_exc
    except JWTError:
        raise cred_exc

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise cred_exc
    return user

# 导出给 main.py 使用
public_router = router
