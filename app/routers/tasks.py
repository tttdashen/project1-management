# app/routers/tasks.py

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate

from app.database import get_db
from app import models
from app.schemas import TaskCreate, TaskOut, Msg
from app.auth_deps import current_user, admin_only
from app.dependencies.cache import cache
from app.middlewares.limiter import limiter

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=TaskOut)
@limiter.limit("10/minute")
def create_task(
    request: Request,
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(current_user),
):
    data = task_in.model_dump()
    data["owner_id"] = user.id
    task = models.Task(**data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("", response_model=Page[TaskOut])
@cache(expire=30)
def list_tasks(
    _user: models.User = Depends(current_user),
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    order_by: str = Query("id"),
    desc_: bool = Query(False, alias="desc"),
    is_done: Optional[bool] = Query(None),
):
    """
    直接对 SQLAlchemy Query 对象进行分页，而不是先 .all() 再 paginate。
    """
    # 1. 构造 Query
    query = db.query(models.Task)
    if is_done is not None:
        query = query.filter(models.Task.is_done == is_done)

    # 2. 排序
    order_col = getattr(models.Task, order_by, models.Task.id)
    query = query.order_by(desc(order_col) if desc_ else order_col)

    # 3. 计算分页参数并返回
    page_params = Params(size=limit, page=offset // limit + 1)
    return paginate(query, params=page_params)

@router.get("/{task_id}", response_model=TaskOut, responses={404: {"model": Msg}})
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(current_user),
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.owner_id == user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task

@router.get(
    "/admin/{task_id}",
    response_model=TaskOut,
    responses={403: {"model": Msg}, 404: {"model": Msg}}
)
def admin_get_task(
    task_id: int,
    db: Session = Depends(get_db),
    _admin: models.User = Depends(admin_only),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task
