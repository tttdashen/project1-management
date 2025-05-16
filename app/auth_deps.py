"""
常用依赖:
- current_user : 必须带合法 JWT
- admin_only   : 额外要求 is_admin=True
"""
from fastapi import Depends, HTTPException, status
from app.auth import get_current_user
from app.schemas import UserOut

# ---------------- 必须登录 ----------------
def current_user(
    user: UserOut | None = Depends(get_current_user)
) -> UserOut:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# ---------------- 仅管理员 ----------------
def admin_only(
    user: UserOut = Depends(current_user),
) -> UserOut:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user
