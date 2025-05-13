# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

# ---------- 任务相关 ----------
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=50, description="任务标题，1‑50 字符")
    description: Optional[str] = Field(None, max_length=200, description="任务描述，最多 200 字符")


class Task(TaskCreate):
    id: int
    class Config:                       # pydantic v1 写法
        orm_mode = True                 # v2 可改为 model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token:str
    token_type:str="bearer"
    
# ---------- 用户相关 ----------
class UserCreate(BaseModel):            # 请求体：注册用户
    username: str
    password: str

class UserOut(BaseModel):                  # 响应体：返回给前端，不含密码
    id: int
    username: str
    class Config:
        orm_mode = True
