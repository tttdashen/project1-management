import os, sys, pytest
from fastapi.testclient import TestClient

# ---- 让解释器找到 app 包 ----
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, PROJECT_ROOT)

# ---- 导入 FastAPI 实例，用别名避免覆盖包名 ----
from app.main import app as fastapi_app
from app.database import Base, engine, SessionLocal
import app.models  # 注册表


# ---------- 每个测试函数前后重建数据库 ----------
@pytest.fixture(autouse=True, scope="function")
def fresh_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ---------- Session fixture ----------
@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- TestClient ----------
@pytest.fixture
def client():
    with TestClient(fastapi_app) as c:
        yield c
