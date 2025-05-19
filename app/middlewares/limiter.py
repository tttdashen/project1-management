"""
SlowAPI 限流中间件
- 在 main.py 启动时调用 init_limiter(app)
- 在路由上用 @limiter.limit("10/minute")
"""

from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# ---------- 新 key_func ----------
def token_or_ip(request: Request) -> str:
    """
    · 若请求带 Authorization 头（JWT / Bearer token），用其作为限流键；
    · 否则退回到客户端 IP（TestClient 场景为 "testclient"）。
    这样不同登录用户互不影响，测试用例也不会串桶。
    """
    auth = request.headers.get("Authorization")
    return auth or get_remote_address(request)


# 实例化 Limiter
limiter = Limiter(key_func=token_or_ip)

def init_limiter(app: FastAPI) -> None:
    """在 FastAPI 启动时调用，注册限流器 & 异常处理"""
    app.state.limiter = limiter
    app.add_exception_handler(
        RateLimitExceeded, _rate_limit_exceeded_handler
    )
