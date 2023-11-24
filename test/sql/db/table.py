from sqlalchemy import Index, Integer, String, Column, DateTime, PrimaryKeyConstraint, UniqueConstraint, \
    ForeignKeyConstraint
from datetime import datetime
from .base import Base


class User2(Base):
    __tablename__ = 'users2'
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(200), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_pk'),
        UniqueConstraint('username'),
        UniqueConstraint('email'),
    )


class Post2(Base):
    __tablename__ = 'posts2'
    title = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    content = Column(String(50), nullable=False)
    published = Column(String(200), nullable=False, default=False)
    user_id = Column(Integer(), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users2.id']),
        Index('title_content_index' 'title', 'content'),  # composite index on title and content
    )
