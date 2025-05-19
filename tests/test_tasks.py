# tests/test_tasks.py
from starlette import status


def test_creat_task(client, auth_header):
    payload = {"title": "写测试用例", "description": "学习如何测试FastAPI接口"}
    resp = client.post("/tasks", json=payload, headers=auth_header)
    assert resp.status_code in (status.HTTP_200_OK, status.HTTP_201_CREATED)
    data = resp.json()
    assert data["title"] == payload["title"]
    assert "id" in data


def test_get_task(client, auth_header):
    # 先创建一条任务
    create = client.post(
        "/tasks",
        json={"title": "查询测试", "description": "测试 get_task 接口"},
        headers=auth_header,
    )
    assert create.status_code in (200, 201)
    task_id = create.json()["id"]

    # 查询
    get_r = client.get(f"/tasks/{task_id}", headers=auth_header)
    assert get_r.status_code == status.HTTP_200_OK
    assert get_r.json()["id"] == task_id


def test_get_invalid_task(client, auth_header):
    resp = client.get("/tasks/999999", headers=auth_header)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
