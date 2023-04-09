from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey

from src.user.models import User
from src.database import Base


class Article(Base):
    __tablename__ = 'article'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(125), unique=True, index=True, nullable=False)
    conten: Mapped[str] = mapped_column(String)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped[User] = relationship('User')