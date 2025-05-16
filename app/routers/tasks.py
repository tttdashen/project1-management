# ❶ 去掉 postponed-annotations —— 不再使用: from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from fastapi_pagination import Page, paginate, Params
from typing import Optional

from app.database import get_db
from app import models
from app.schemas import TaskCreate, TaskOut, Msg
from app.auth_deps import current_user, admin_only
from app.dependencies.cache import cache
from app.middlewares.limiter import limiter

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# -------------------------------------------------- 创建任务 --------------------------------------------------
@router.post("", response_model=TaskOut)
@limiter.limit("10/minute")                     # 每 IP 每分钟 10 次
def create_task(
    request: Request,                           # SlowAPI 用于取 IP
    task_in: TaskCreate,                        # 唯一 JSON 体
    db:   Session      = Depends(get_db),
    user: models.User  = Depends(current_user), # 必须登录
):
    data = task_in.model_dump()
    data["owner_id"] = user.id
    task = models.Task(**data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# -------------------------------------------------- 列表任务 --------------------------------------------------
@router.get("", response_model=Page[TaskOut])
@cache(expire=30)                               # 30 秒缓存
def list_tasks(
    _user: models.User = Depends(current_user),
    db: Session = Depends(get_db),
    limit : int  = Query(10, ge=1, le=100),
    offset: int  = Query(0,  ge=0),
    order_by: str  = Query("id"),
    desc_:   bool  = Query(False, alias="desc"),
    is_done: Optional[bool] = Query(None),
):
    stmt = select(models.Task)
    if is_done is not None:
        stmt = stmt.where(models.Task.is_done == is_done)

    order_col = getattr(models.Task, order_by, models.Task.id)
    stmt = stmt.order_by(desc(order_col) if desc_ else order_col)

    tasks = db.execute(stmt).scalars().all()
    page_params = Params(size=limit, page=offset // limit + 1)
    return paginate(tasks, params=page_params)

# -------------------------------------------------- 获取本人任务 --------------------------------------------------
@router.get("/{task_id}", response_model=TaskOut, responses={404: {"model": Msg}})
def get_task(
    task_id: int,
    db:   Session      = Depends(get_db),
    user: models.User  = Depends(current_user),
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.owner_id == user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task

# -------------------------------------------------- 管理员读取任务 --------------------------------------------------
@router.get("/admin/{task_id}",
            response_model=TaskOut,
            responses={403: {"model": Msg}, 404: {"model": Msg}})
def admin_get_task(
    task_id: int,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(admin_only),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task
