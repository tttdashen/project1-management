from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from .. import models,schemas,database

router = APIRouter()

#获取数据库对话
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks",response_model=schemas.Task)
def creat_task(task:schemas.TaskCreate,db:Session=Depends(get_db)):
    if task.title.strip()=="":
        raise HTTPException(status_code=400,detail="任务标题不能为空")
    #判断标题是否包含非法字符（如全是空格）
    db_task=models.TaskDB(title=task.title,description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks/{task_id}",response_model=schemas.Task)
def get_task(task_id:int,db:Session=Depends(get_db)):
    task = db.query(models.TaskDB).filter(models.TaskDB.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404,detail="任务不存在")
    return task
