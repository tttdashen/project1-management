from typing import Optional
from pydantic import BaseModel, ConfigDict


# -------- 用户 --------
class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True, extra="ignore")


# -------- 任务 --------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int
    is_done: bool
    owner_id: Optional[int] = None  # 允许空

    model_config = ConfigDict(from_attributes=True, extra="ignore")


# -------- 其他 --------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Msg(BaseModel):
    detail: str
