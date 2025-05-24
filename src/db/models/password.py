from src.db.models.base import Base
from sqlalchemy import String, Column, BLOB, Integer

class Password(Base):
    __tablename__ = "passwords"

    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String, nullable=False)
    login: Column = Column(String, nullable=False)
    password: Column = Column(BLOB, nullable=False)