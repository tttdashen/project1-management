# #day1
# from fastapi import FastAPI #调用函数，fastapi是文件名（不含.py），FastAPI是函数名
# from typing import List
# from models import TaskCreat,Task  #调用我创建的py
# # 创建 FastAPI 应用实例
# app = FastAPI()

# # ⛓ 用来保存任务的“假数据库”
# tasks:List[Task]=[]# 相当于我们定义了一个列表，专门用来存所有的任务对象（模拟数据库）tasks = []
# task_id_counter=1# 用来为每个任务分配唯一的 ID，每次新建任务，就让 ID +1，确保不会重复。


# @app.post("/tasks",response_model=Task)
# # 定义一个 POST 请求，路径是 /tasks
# # 告诉 FastAPI：请求体是 TaskCreate，响应体是 Task

# def creat_task(task:TaskCreat):
#     # 接收请求体的 JSON，会自动变成一个 TaskCreate 对象
#     # 例如 JSON 为 {"title": "买菜", "description": "买鸡蛋"}
# #FastAPI 会自动做这些事：类型校验（title 是否为字符串）缺少字段会返回 422 错误
#     global task_id_counter## 引用上面的全局变量 task_id_counter（否则函数内不能修改它）
#     new_task = Task(id=task_id_counter, **task.dict())  # 合并 ID 和用户提交字段
#     # 把 Pydantic 对象 task 转换成普通字典
#     # 例如变成 {'title': '买菜', 'description': '买鸡蛋'}

#     task_id_counter += 1
#     tasks.append(new_task)
#     return new_task
# @app.get("/tasks",response_model=List[Task])
# def get_all_tasks():
#     """
#     获取所有任务列表（GET 方法）
#     返回存储在内存中的任务数组
#     """
#     return tasks

# @app.get('/hello')#定义一个路径为/hello的get请求接口，当浏览器访问 http://127.0.0.1:8000/hello 时，就会触发绑定的那个函数执行。
# def read_hello():
#     # 接口返回 JSON 数据
#     return {'message':'Hello world'}
# '''
# 示例：欢迎接口
# @app.get('/hello')
# def say_hello():
#     return {'msg':'Hello FastAPI!'}
# 访问 /hello,返回
# {"msg": "Hello FastAPI!"}

# 示例：获取用户姓名
# @app.get('/user/name')
# def get_user(name:str):
#     return {'username':name}
# 访问 /user/jack，返回：
# {"username": "jack"}
# '''
# #day2
# #步骤一：定义路径参数接口
# @app.get("/users/{user_id}")#/users/{user_id}：路径中带变量
# def read_user(user_id:int):#user_id: int：自动转换类型，访问 /users/123 会传入 123#
#     return{"user_id":user_id}#FastAPI 会自动帮你处理参数类型，错误类型（如 /users/abc）会返回 422 错误

# #步骤二：定义带查询参数的接口
# @app.get("/items")
# def read_items(skip:int=0,limit:int=10):#可以设置默认值，不传参数也不会报错
#     #访问 /items/?skip=5&limit=20.skip 和 limit 是查询参数（URL 中 ? 后面的部分）
#     return{"skip":skip,"limit":limit}

# @app.get("/books/{book_id}")
# def get_book(book_id:int,detail:bool=False):#要求输入的book_id为整数型，输入的datail为布尔型
#     return{"book_id":book_id,"detail":detail}



#day2.2重新写完整代码
# main.py
# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from pydantic import BaseModel
# from typing import Optional, List
# from database import SessionLocal, init_db
# from models import TaskDB

# app = FastAPI()
# init_db()  # 初始化数据库

# # ---- Pydantic 数据模型 ----
# class TaskCreate(BaseModel):
#     title: str
#     description: Optional[str] = None

# class Task(TaskCreate):
#     id: int

#     class Config:
#         orm_mode = True  # 关键：让 Pydantic 支持 ORM 模型

# # ---- 数据库 Session 获取器 ----
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # ---- 创建任务接口 ----
# @app.post("/tasks", response_model=Task)
# def create_task(task: TaskCreate, db: Session = Depends(get_db)):
#     new_task = TaskDB(title=task.title, description=task.description)
#     db.add(new_task)
#     db.commit()
#     db.refresh(new_task)
#     return new_task

# # ✅ ---- 查询指定任务接口 ----
# @app.get("/tasks/{task_id}", response_model=Task)
# def get_task(task_id: int, db: Session = Depends(get_db)):
#     task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
#     if not task:
#         raise HTTPException(status_code=404, detail=f"任务 ID {task_id} 不存在")
#     return task

#day4-- app/main.py — 入口文件（非常简洁）
# app/main.py
from fastapi import FastAPI
from app.database import Base, engine
from app import models       
from config import settings
      


Base.metadata.create_all(bind=engine)

# 初始化数据库
from app.routers import tasks, users
app = FastAPI()
app.include_router(tasks.router)  # 注册 /tasks 路由模块
app.include_router(users.router)#新增注册用户接口

@app.get("/") 
def read_root():
    return{
        "message": "任务系统启动成功",
        "environment": settings.APP_ENV
    }
