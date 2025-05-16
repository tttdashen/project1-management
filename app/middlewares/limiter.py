"""
SlowAPI 限流中间件
在 main.py startup: init_limiter(app)
在具体路由: @limiter.limit("10/minute")
"""
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# 仅保留 key_func，其他保持默认
limiter = Limiter(key_func=get_remote_address)

def init_limiter(app: FastAPI):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
