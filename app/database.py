from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = "sqlite:///./tasks.db"

# 创建 SQLite 数据库连接（tasks.db）
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 创建会话工厂，用于后续操作数据库（插入、查询等）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 初始化数据库（创建表结构）
def init_db():
    Base.metadata.create_all(bind=engine)

'''你可以把 database.py 看作是“数据库接线板”：
- 帮你插好电源（engine）
- 准备好工具箱（SessionLocal）
- 创建好桌子（数据库表结构）'''