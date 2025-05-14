from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_creat_task():
    payload = {"title": "写测试用例", "description": "学习如何测试FastAPI接口"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 200


def test_get_task():
    response = client.post(
        "/tasks",
        json={"title": "查询测试", "description": "测试get_task接口"},
    )
    task_id = response.json()["id"]
    response_get = client.get(f"/tasks/{task_id}")
    assert response_get.status_code == 200
    assert response_get.json()["title"] == "查询测试"


def test_get_invalid_task():
    response = client.get("/tasks/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "任务不存在"}
