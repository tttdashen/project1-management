# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.database import get_db
from app.schemas import UserCreate, UserOut, Msg
from app import models

router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
    "",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": Msg}},
)
def register_user(
    payload: UserCreate,
    db:      Session   = Depends(get_db),
):
    """
    注册新用户；用户名重复返回 400。
    用户名为 'root' 自动赋予 is_admin=True。
    """
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")

    user = models.User(
        username=payload.username,
        password=bcrypt.hash(payload.password),
        is_admin=(payload.username == "root"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# 导出 router 给 main.py 使用
users_router = router
