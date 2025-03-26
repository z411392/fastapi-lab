from fastapi_lab.orm.models.general.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    orders = relationship("Order", back_populates="user")
