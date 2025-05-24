from src.db.models.base import Base
from sqlalchemy import String, Column, BLOB, Integer

class Meta(Base):
    __tablename__ = "meta"

    id: Column = Column(Integer, primary_key=True, default=1)
    salt: Column = Column(BLOB, nullable=False)
    kdf_iter: Column = Column(Integer, nullable=False)
    verify_token: Column = Column(BLOB, nullable=False)