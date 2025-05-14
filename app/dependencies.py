from fastapi import Depends,HTTPException,status
from app.auth import get_current_user
from app.schemas import UserOut

def current_user(
        user:UserOut=Depends(get_current_user)       
)->UserOut:
    """
    作用：强制所有任务接口都必须携带合法 JWT，并返回当前用户信息
    """
    return user

def admin_only(
        user:UserOut=Depends(get_current_user)
)->UserOut:
    """
    作用：仅允许 is_admin=True 的用户访问，其他抛 403
    """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return user