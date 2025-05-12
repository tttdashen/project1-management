from pydantic import BaseModel,Field
from typing import Optional

class TaskCreate(BaseModel):
    title:str = Field(...,min_length=1,max_length=50,description="任务标题，1-50字符")
    # Field(...) 表示这是必填字段，并附加了长度验证和说明，Swagger UI 也会自动展示限制。
    description:Optional[str]=Field(None,max_length=200,description="任务描述，最多200字符")

class Task(TaskCreate):
    id:int

    class Config:
        orm_mode=True