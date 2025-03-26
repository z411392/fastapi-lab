from fastapi_lab.orm.models.general.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    in_stock = Column(Boolean, default=True)
