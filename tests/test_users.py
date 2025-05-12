from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_register_user_success():
    response=client.post("/users",json={
        "username":"tanlongfei",
        "password":"23"
    })
    assert response.status_code==200
    data = response.json()
    assert data["username"]=='tanlongfei'
    assert "id" in data

def test_register_user_duplicate():
    #重复注册同一用户
    client.post("/users",json={"username":"dupe_user","password":"123"})
    response=client.post("/users",json={"username": "dupe_user", "password": "456"})
    assert response.status_code==400
    assert response.json()=={"detail":"用户名已存在"}