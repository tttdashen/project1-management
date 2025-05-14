from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)

    tasks = relationship(
        "Task", back_populates="owner", cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255))
    is_done = Column(Boolean, default=False)

    owner_id = Column(  # Day 9 先允许空，Day 10 写入真实用户
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )

    owner = relationship("User", back_populates="tasks")
