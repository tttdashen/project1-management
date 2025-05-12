# #定义 Pydantic 数据模型
# '''
# pydantic是FastAPI底层用来数据校验的工具，它可以：
# | 功能     | 举例                              |
# | ------ | ------------------------------- |
# | 自动类型校验 | `title: str` 传数字就报错             |
# | 自动生成文档 | Swagger 会显示 `title` 是 string，必填 |
# | 自动转换   | 传 `"123"` 也能转成 int              |
# | 自动提示   | 文档界面会提示字段说明和格式                  |

# '''
# from pydantic import BaseModel#调用pydantic里面的一个自动检验的函数
# from typing import Optional

# '''
# 这相当于你定义了一个「数据模子」，告诉 FastAPI：

# 我要接收的 JSON 数据长这个样子！'''
# class TaskCreat(BaseModel):#定义字典，引用继承 Pydantic 的基类，启用自动校验功能
#     title:str              #用户必须传一个字符串字段title # 任务标题（必填）
#     description:Optional[str]=None #这个字段是可选的，不填就是 None

# #这个是「响应数据结构」：，直接继承TaskCreate，减少重复代码。
# #它的意思是：响应体和请求体几乎一样，只是多了一个 ID 字段。
# class Task(TaskCreat):#这个是响应
#     id:int

# #在day2.2就已经不调用这个上面py了，因为直接写进mian了


#创建ORM模型
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()  # 创建 ORM 基类，所有模型必须继承它

class TaskDB(Base):
    __tablename__ = "tasks"  # 数据表名称
    __table_args__ = {'extend_existing': True}  # 解决重复表定义的问题
    id = Column(Integer, primary_key=True, index=True)      # 主键，自动递增
    title = Column(String, index=True)                      # 标题字段
    description = Column(String, nullable=True)             # 描述字段，可为空

#✅ 新增：用户模型
class UserDB(Base):
    __tablename__="users"
    __table_args__ = {'extend_existing': True}  
    id = Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True)# # 用户名不能重复
    password=Column(String)## 这里简单用明文密码，Day9会改成哈希




'''
TaskDB 类就像是你在 Excel 中创建了一张任务表：
- 每一列是字段（id, title, description）
- 每一行是一个任务记录
- 每个字段的类型和约束，在 Column 中定义
'''