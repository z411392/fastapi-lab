from os import getenv
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    func,
    Boolean,
    Text,
    text,
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import relationship, declarative_base
import pytest

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "test_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())

    orders = relationship("OrderModel", back_populates="user")


class ProductModel(Base):
    __tablename__ = "test_products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    in_stock = Column(Boolean, default=True)


class OrderModel(Base):
    __tablename__ = "test_orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("test_users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("test_products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=func.now())

    user = relationship("UserModel", back_populates="orders")
    product = relationship("ProductModel")


class LogModel(Base):
    __tablename__ = "test_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    event = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())


@pytest.mark.skip
class TestSQLAlchemy:
    @pytest.fixture(scope="function")
    async def db_session(self):
        engine = create_async_engine(getenv("DATABASE_URL"), echo=False, future=True)
        async_session = async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        async with async_session() as read_session, async_session() as write_session:
            yield read_session, write_session
        async with engine.begin() as connection:
            for table in reversed(Base.metadata.sorted_tables):
                if table.name.startswith("test_"):
                    await connection.execute(table.delete())
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_create_user(self, db_session):
        read_session, write_session = db_session
        user = UserModel(username="testuser", email="test@example.com")
        write_session.add(user)
        await write_session.commit()

        result = await read_session.execute(text("SELECT COUNT(*) FROM test_users"))
        count = result.scalar()
        assert count == 1

    @pytest.mark.asyncio
    async def test_create_product(self, db_session):
        read_session, write_session = db_session
        product = ProductModel(name="Test Product", price=100)
        write_session.add(product)
        await write_session.commit()

        result = await read_session.execute(text("SELECT COUNT(*) FROM test_products"))
        count = result.scalar()
        assert count == 1

    @pytest.mark.asyncio
    async def test_create_order(self, db_session):
        read_session, write_session = db_session
        user = UserModel(username="testuser", email="test@example.com")
        product = ProductModel(name="Test Product", price=100)
        write_session.add_all([user, product])
        await write_session.commit()

        order = OrderModel(user_id=user.id, product_id=product.id, quantity=2)
        write_session.add(order)
        await write_session.commit()

        result = await read_session.execute(text("SELECT COUNT(*) FROM test_orders"))
        count = result.scalar()
        assert count == 1

    @pytest.mark.asyncio
    async def test_create_log(self, db_session):
        read_session, write_session = db_session
        log = LogModel(
            event="User logged in", details="User testuser logged in successfully"
        )
        write_session.add(log)
        await write_session.commit()

        result = await read_session.execute(text("SELECT COUNT(*) FROM test_logs"))
        count = result.scalar()
        assert count == 1
