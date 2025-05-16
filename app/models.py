from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Index   # ✏️ 删除: 未导入 DateTime
# ✏️ 删除 from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
import datetime                                  # ➕

from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255))
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)   # ➕ 供排序
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    owner = relationship("User", back_populates="tasks")

    # ➕ 新索引：提高分页 + 过滤性能
    __table_args__ = (
        Index("idx_done_created", "is_done", "created_at"),
    )
