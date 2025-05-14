from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_and_login():
    # 注册
    r = client.post("/users", json={"username": "alice", "password": "pwd"})
    assert r.status_code == 201
    uid = r.json()["id"]

    # 重复注册
    r_dup = client.post("/users", json={"username": "alice", "password": "pwd"})
    assert r_dup.status_code == 400

    # 登录成功
    token_resp = client.post(
        "/login",
        data={"username": "alice", "password": "pwd"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert token_resp.status_code == 200
    token = token_resp.json()["access_token"]
    assert token

    # 创建任务
    task_resp = client.post(
        "/tasks",
        json={"title": "pytest 任务", "description": "自动化测试"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert task_resp.status_code == 200
    task_id = task_resp.json()["id"]

    # 获取列表
    list_resp = client.get("/tasks")
    assert any(t["id"] == task_id for t in list_resp.json())


def test_wrong_password():
    client.post("/users", json={"username": "bob", "password": "123"})
    r = client.post(
        "/login",
        data={"username": "bob", "password": "wrong"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "密码错误"
