from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/tasks", tags=["tasks"])

# ---------- 创建 ----------
@router.post("", response_model=schemas.Task, status_code=status.HTTP_200_OK)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = models.Task(**task_in.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# ---------- 列表 ----------
@router.get("", response_model=list[schemas.Task])    # ★ 一定是 list[schemas.Task]
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()              # ★ 返回真实列表
    return tasks

# ---------- 单条查询 ----------
@router.get("/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task
