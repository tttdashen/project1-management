import time, pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_pagination_and_cache(client):
    """
    1) 第一次查询返回 200
    2) 同参数第二次明显更快（命中缓存）
    3) limit=1 时只返回一条数据
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        t0 = time.perf_counter()
        r1 = await ac.get("/tasks", params={"limit": 1})
        t1 = time.perf_counter()
        r2 = await ac.get("/tasks", params={"limit": 1})
        t2 = time.perf_counter()

    assert r1.status_code == 200 and r2.status_code == 200
    assert len(r1.json()["items"]) == 1
    assert (t1 - t0) > (t2 - t1)          # 第二次应更快

@pytest.mark.asyncio
async def test_rate_limit(client):
    """连续 11 次 POST，应最后一次 429"""
    headers = {}
    for _ in range(10):
        client.post("/tasks", json={"title": "spam"}, headers=headers)
    r = client.post("/tasks", json={"title": "overflow"}, headers=headers)
    assert r.status_code == 429
