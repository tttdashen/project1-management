from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import TaskCreate, TaskOut, Msg
from app.auth import get_current_user  # Day 10 权限

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskOut)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    user: models.User | None = Depends(get_current_user),  # 无 token 时 user=None
):
    data = task_in.model_dump()
    if user:
        data["owner_id"] = user.id
    task = models.Task(**data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


@router.get("/{task_id}", response_model=TaskOut, responses={404: {"model": Msg}})
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: models.User | None = Depends(get_current_user),
):
    q = db.query(models.Task).filter(models.Task.id == task_id)
    if user and not user.is_admin:
        q = q.filter(models.Task.owner_id == user.id)
    task = q.first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


# 管理员可访问所有
@router.get("/admin/{task_id}", response_model=TaskOut, responses={404: {"model": Msg}})
def admin_get_task(
    task_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_user),
):
    if not admin or not admin.is_admin:
        raise HTTPException(status_code=403, detail="无权限")
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task
