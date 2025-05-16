"""
自动选择缓存后端：
- 若本地 6379 端口 Redis 可连通 → RedisBackend
- 否则回退 InMemoryBackend
不再依赖 aioredis，改用 redis.asyncio
"""
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.inmemory import InMemoryBackend
import redis.asyncio as redis          # ✅ 新：官方异步客户端
import logging
import asyncio

async def init_cache(app: FastAPI) -> None:  # type: ignore[override]
    try:
        r = await redis.from_url(
            "redis://localhost:6379",   # 1 秒连不上就超时
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=1,
        )
        await r.ping()                 # 测试连通
        backend = RedisBackend(r)
        logging.info("✅ fastapi-cache 使用 Redis 后端")
    except Exception as exc:
        backend = InMemoryBackend()
        logging.warning("⚠️ Redis 不可用，已退化为 InMemory 缓存: %s", exc)

    FastAPICache.init(backend, prefix="task-cache")

def cache(expire: int = 60):
    from fastapi_cache.decorator import cache as _cache
    return _cache(expire=expire)
