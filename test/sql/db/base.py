from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    id = Column(Integer, primary_key=True, autoincrement=False)
