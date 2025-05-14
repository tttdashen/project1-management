# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import TaskCreate, TaskOut, Msg
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=TaskOut)
def create_task(
    task_in: TaskCreate,
    db:      Session          = Depends(get_db),
    user:    models.User | None = Depends(get_current_user),
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
    db:      Session          = Depends(get_db),
    user:    models.User | None = Depends(get_current_user),
):
    query = db.query(models.Task).filter(models.Task.id == task_id)
    if user and not user.is_admin:
        query = query.filter(models.Task.owner_id == user.id)
    task = query.first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task

@router.get("/admin/{task_id}", response_model=TaskOut, responses={403:{"model":Msg},404:{"model":Msg}})
def admin_get_task(
    task_id: int,
    db:      Session          = Depends(get_db),
    user:    models.User | None = Depends(get_current_user),
):
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="无权限")
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task
