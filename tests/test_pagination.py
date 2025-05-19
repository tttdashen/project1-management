# tests/test_pagination.py
"""
分页 / 缓存 & 限流测试（同步 TestClient）
"""

import time
from starlette import status
import pytest


def test_pagination_and_cache(client, auth_header):
    """
    1. 先创建 1 条任务，保证列表非空
    2. 连续两次相同查询，第二次命中缓存 → 响应更快
    """
    client.post("/tasks", json={"title": "缓存测试"}, headers=auth_header)

    t0 = time.perf_counter()
    r1 = client.get("/tasks", params={"limit": 1}, headers=auth_header)
    t1 = time.perf_counter()
    r2 = client.get("/tasks", params={"limit": 1}, headers=auth_header)
    t2 = time.perf_counter()

    assert r1.status_code == status.HTTP_200_OK
    assert r2.status_code == status.HTTP_200_OK
    assert len(r1.json()["items"]) == 1
    assert (t1 - t0) > (t2 - t1)           # 第 2 次更快（缓存）


@pytest.mark.asyncio
async def test_rate_limit(client, auth_header):
    """
    连续 11 次 POST：
    · 前 10 次正常
    · 第 11 次触发限流 → 429
    """
    for _ in range(10):
        client.post("/tasks", json={"title": "spam"}, headers=auth_header)
    last = client.post("/tasks", json={"title": "overflow"}, headers=auth_header)
    assert last.status_code == status.HTTP_429_TOO_MANY_REQUESTS
