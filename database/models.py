from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(150), nullable=False)
    first_name = Column(String(150))
    last_name = Column(String(150))
    password = Column(String(150), nullable=False)
    active = Column(Boolean, default=False)
    registered = Column(DateTime, default=datetime.utcnow)


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    content = Column(String)
    created = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')




