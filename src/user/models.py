from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Role(Base):
    __tablename__ = 'role'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(125), unique=True, nullable=False)


class User(SQLAlchemyBaseUserTable, Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False)
    first_name: Mapped[str] = mapped_column(String(125), nullable=True)
    last_name: Mapped[str] = mapped_column(String(125), nullable=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'))
    role: Mapped[Role] = relationship()
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    registered: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
