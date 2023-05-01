from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base
from src.user.models import User


class Article(Base):
    __tablename__ = 'article'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(125), unique=True, index=True, nullable=False)
    conten: Mapped[str] = mapped_column(String)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped[User] = relationship('User')
    comments: Mapped[List['Comment']] = relationship(back_populates="article", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(150), nullable=False)
    article_id: Mapped[int] = mapped_column(ForeignKey('article.id'))
    article: Mapped[Article] = relationship(back_populates="comments")
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped[User] = relationship('User')
