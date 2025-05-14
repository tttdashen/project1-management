from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.routers.users import SECRET_KEY, ALGORITHM

# auto_error=False ➜ 若缺少 Authorization 头，将返回 None 而不是抛 401
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User | None:
    """
    若请求未携带 Bearer Token → 返回 None
    若携带 Token 但无效 → 抛 401
    """
    if not token:  # 无 token，视为匿名
        return None

    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise cred_exc
    except JWTError:
        raise cred_exc

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise cred_exc
    return user
