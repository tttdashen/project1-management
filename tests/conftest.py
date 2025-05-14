import os
import sys
import pytest
from fastapi.testclient import TestClient

# 让 pytest 能找到你的 app 包
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, PROJECT_ROOT)

# 在导入任何 app 代码前，确保模块加载了模型
import app.models  # noqa: F401

# 从 app.main 导入 FastAPI 实例，别名 application，避免与包名冲突
from app.main import app as application
from app.database import Base, engine, SessionLocal


@pytest.fixture(autouse=True, scope="function")
def fresh_db():
    """
    每个测试函数前后都重建数据库，
    先 drop_all，再 create_all，测试结束后再 drop_all。
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """提供一个 SQLAlchemy Session 用于访问数据库"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """
    提供一个带生命周期管理的 TestClient 实例。
    注意这里使用的是 application（FastAPI 实例），而不是模块。
    """
    with TestClient(application) as c:
        yield c
