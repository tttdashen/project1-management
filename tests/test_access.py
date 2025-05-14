def test_acl_owner_and_admin(client, db_session):
    # client, db_session fixture 来自 Day9 已有配置
    # 1. 注册三位用户
    client.post("/users", json={"username": "alice", "password": "pwd"})
    client.post("/users", json={"username": "bob",   "password": "pwd"})
    client.post("/users", json={"username": "root",  "password": "pwd"})  # root is_admin=True

    # 2. alice 登录并创建任务
    token_a = client.post("/login", data={"username":"alice","password":"pwd"}).json()["access_token"]
    h_a = {"Authorization": f"Bearer {token_a}"}
    tid = client.post("/tasks", json={"title":"T1","description":"d"}, headers=h_a).json()["id"]

    # 3. bob 登录尝试访问 alice 的任务 ➜ 应 404
    token_b = client.post("/login", data={"username":"bob","password":"pwd"}).json()["access_token"]
    h_b = {"Authorization": f"Bearer {token_b}"}
    r = client.get(f"/tasks/{tid}", headers=h_b)
    assert r.status_code == 404

    # 4. root 登录访问 admin 路由 ➜ 应 200
    token_r = client.post("/login", data={"username":"root","password":"pwd"}).json()["access_token"]
    h_r = {"Authorization": f"Bearer {token_r}"}
    r2 = client.get(f"/tasks/admin/{tid}", headers=h_r)
    assert r2.status_code == 200
