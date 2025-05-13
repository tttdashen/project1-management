"""
database.py
-----------------------------------
统一管理数据库引擎、Base，以及 FastAPI 的 Session 依赖。
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite 数据库（保持与之前一致即可）
SQLALCHEMY_DATABASE_URL = "sqlite:///./task_manager.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # 仅 SQLite 需要
)

# SessionLocal: 每个请求独享的数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 所有 ORM 模型基类
Base = declarative_base()


# ✅ 新增：FastAPI 依赖，用于在路由函数里拿到 db
def get_db():
    """
    生成一个数据库会话 (Session)，请求结束自动关闭。
    用法：
        from app.database import get_db
        def route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
