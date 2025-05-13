
from fastapi.testclient import TestClient
from app.main import app
#创建一个测试客户端（模拟浏览器访问）
client = TestClient(app)

## ✅ 测试 POST /tasks 创建任务接口
def test_creat_task():
    #构造请求JSON
    payload={
        "title":"写测试用例",
        "description":"学习如何测试FastAPI接口"
    }

#发送post的请求到/tasks接口
    response = client.post("/tasks",json=payload)


# 断言 HTTP 响应码为 200
    assert response.status_code==200

#获取返回后的json数据
    data = response.json()

#检查返回的字段是否符合预期
    assert data["title"]=="写测试用例"
    assert data["description"]=="学习如何测试FastAPI接口"
    assert "id" in data #id是自动生成的

## ✅ 测试 GET /tasks/{id} 查询任务接口
def test_get_task():
    #先创建一个任务
    response=client.post("/tasks",json={
        "title":"查询测试",
        "description":"测试get_task接口"
    })
    task = response.json()
    task_id=task["id"]

    # 发起 GET 请求查询这个任务
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code==200

    # 校验返回字段
    data = response.json()
    assert data["title"] == "查询测试"
    assert data["description"] == "测试get_task接口"

#❌ 测试查询不存在任务
def test_get_invalid_task():
    response = client.get("/tasks/99999")  # 任务 ID 不存在
    assert response.status_code == 404
    assert response.json() == {"detail": "任务不存在"}