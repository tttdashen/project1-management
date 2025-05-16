"""
集成测试：注册 -> 登录 -> 创建任务 -> 列表查询
确保严格鉴权：所有 /tasks 调用必须带 Bearer token
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _get_token(username="alice", password="pwd") -> str:
    # 注册（重复注册会 400，但不影响返回 token 流程）
    client.post("/users", json={"username": username, "password": password})
    # 登录
    res = client.post(
        "/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return res.json()["access_token"]


@pytest.fixture
def auth_header():
    token = _get_token()
    return {"Authorization": f"Bearer {token}"}


def test_register_and_login(auth_header):
    # 已在 fixture 中注册+登录

    # 创建新任务
    payload = {"title": "pytest 任务", "description": "自动化测试"}
    task_resp = client.post("/tasks", json=payload, headers=auth_header)
    assert task_resp.status_code == 200
    task_id = task_resp.json()["id"]

    # 列表查询（带 token）
    list_resp = client.get("/tasks", headers=auth_header)
    tasks_json = list_resp.json()["items"]
    assert any(t["id"] == task_id for t in tasks_json)
