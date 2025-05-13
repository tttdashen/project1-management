#专门处理 JWT 令牌的生成与验证。
#以后所有需要鉴权的地方，都可以 import 这里的函数。
from datetime import datetime,timedelta
from jose import JWTError,jwt

# ★★★★★ 生产环境一定要把 SECRET_KEY 存进 .env 或 OS 环境变量里！
SECRET_KEY="your-secret-key"
ALGORITHM = "HS256"# 常用对称加密算法
ACCESS_TOKEN_EXPIRE_MINUTES=30# Token 有效期 30 分钟

#创建访问令牌
def create_access_token(data:dict,expires_delta:timedelta|None=None)-> str:#表示函数返回值的类型应该是str
    """
    功能：根据给定数据生成 JWT 字符串。
    参数：
        data — 需要写进令牌载荷(payload)的键值对，如 {"sub": "username"}
        expires_delta — 自定义过期时间，不提供就默认 15 分钟
    """
    to_encode=data.copy() # 不要直接改入参，先拷贝
    expire=datetime.utcnow()+(
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    to_encode.update({"exp":expire}) # JWT 标准字段：到期时间
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#验证和解析令牌
def verify_token(token:str)->dict|None:#表示该函数的返回值类型是 dict（字典）或 None
    """
    功能：解析并校验 JWT。
    成功返回 payload(dict)；失败返回 None。
    """
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None # 统一返回 None，调用方自己决定抛错还是重定向登录