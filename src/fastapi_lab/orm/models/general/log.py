from fastapi_lab.orm.models.general.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    Text,
)


class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    event = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
