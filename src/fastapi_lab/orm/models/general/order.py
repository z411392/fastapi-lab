from fastapi_lab.orm.models.general.base import Base
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    func,
    ForeignKey,
)
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="orders")
    product = relationship("Product")
