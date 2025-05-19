from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

#自定义中间件类:记录处理耗时
class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next)->Response:
        start_time = time.time()
        response = await call_next(Request)
        process_time = time.time()-start_time
        print(f"🕒 请求 {request.method} {request.url.path} 用时:{process_time:.4f}秒")
        return response