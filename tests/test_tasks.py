"""
测试任务接口（需要登录）
流程：
1. 注册 user=alice 密码=pwd
2. 登录获取 token
3. 带 Authorization 头调用 /tasks 相关接口
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _get_token(username="alice", password="pwd") -> str:
    # 注册（幂等：若已存在会 400，不影响）
    client.post("/users", json={"username": username, "password": password})
    # 登录拿 token
    resp = client.post(
        "/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return resp.json()["access_token"]


@pytest.fixture
def auth_header():
    token = _get_token()
    return {"Authorization": f"Bearer {token}"}


def test_creat_task(auth_header):
    payload = {"title": "写测试用例", "description": "学习如何测试FastAPI接口"}
    response = client.post("/tasks", json=payload, headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]


def test_get_task(auth_header):
    create = client.post(
        "/tasks",
        json={"title": "查询测试", "description": "测试get_task接口"},
        headers=auth_header,
    )
    task_id = create.json()["id"]

    r = client.get(f"/tasks/{task_id}", headers=auth_header)
    assert r.status_code == 200
    assert r.json()["id"] == task_id


def test_get_invalid_task(auth_header):
    r = client.get("/tasks/99999", headers=auth_header)
    assert r.status_code == 404
