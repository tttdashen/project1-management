import os, sys, uuid, typing as t
import pytest
from fastapi.testclient import TestClient

# 让 pytest 找到 app
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, PROJECT_ROOT)

# 先导入模型，避免某些循环导入
import app.models  # noqa: F401

from app.main import app as application
from app.database import Base, engine, SessionLocal

# ---------- 数据库干净环境 ----------
@pytest.fixture(autouse=True, scope="function")
def fresh_db():
    """每个测试 function 单独建干净表"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- 全局客户端 ----------
@pytest.fixture
def client() -> TestClient:
    """同步 TestClient；作用域 function，避免限流影响别的测试"""
    with TestClient(application) as c:
        yield c

# ---------- 动态用户 / 免去限流 ----------
def _register_and_login(c: TestClient) -> dict[str, str]:
    """
    为每个测试生成唯一用户，避免速率统计 & 数据冲突
    返回 {"Authorization": "Bearer <jwt>"}
    """
    uname = f"user_{uuid.uuid4().hex[:8]}"
    pwd = "pwd"
    # 注册（允许 409 重复）
    c.post("/users", json={"username": uname, "password": pwd})
    # 登录
    resp = c.post(
        "/login",
        data={"username": uname, "password": pwd},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def auth_header(client) -> dict[str, str]:
    """每个测试获得独立 JWT，避免互相限流"""
    return _register_and_login(client)
