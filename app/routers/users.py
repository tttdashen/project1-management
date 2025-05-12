from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from .. import schemas,models,database

router=APIRouter()


#获取数据库对话
def get_db():
    db= database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users",response_model=schemas.User)
def register_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    #检查用户名是否已经存在
    existing_user=db.query(models.UserDB).filter(models.UserDB.username==user.username).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="用户名已存在")
    
    #创建新用户
    db_user = models.UserDB(username=user.username,password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user