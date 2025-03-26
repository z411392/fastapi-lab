import pytest
from fastapi_lab.container import Container, packages
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession
from dependency_injector.wiring import inject, Provide
from fastapi_lab.orm.models.general.base import Base
from fastapi_lab.orm.models.general.user import User
from fastapi_lab.orm.models.general.log import Log
from fastapi_lab.orm.models.general.product import Product
from fastapi_lab.orm.models.general.order import Order
from sqlalchemy.future import select
from sqlalchemy import func


def modify_table_names(base):
    for table in list(base.metadata.tables.values()):
        table.name = f"test_{table.name}"
        for column in table.columns:
            for fk in column.foreign_keys:
                fk._colspec = f"test_{fk._colspec}"

@pytest.mark.skip
class TestSQLAlchemy:
    @pytest.fixture(autouse=True)
    async def container(self):
        container = Container()
        container.wire(
            packages=packages(),
        )
        container.wire(modules=[__name__])
        yield container
        container.unwire()

    @pytest.fixture(autouse=True)
    async def tables(self, container: Container):
        engine: AsyncEngine = container.engine()
        modify_table_names(Base)
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        yield
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)

    # @pytest.mark.skip
    @inject
    async def test_create_tables(self, engine: AsyncEngine = Provide[Container.engine]):
        async with engine.connect() as connection:
            result = await connection.execute(select(1))
            assert result.scalar() == 1

    # @pytest.mark.skip
    @inject
    async def test_create_user(
        self,
        make_session: async_sessionmaker[AsyncSession] = Provide[
            Container.make_session
        ],
    ):
        async with make_session() as session:
            user = User(username="testuser", email="test@example.com")
            session.add(user)
            await session.commit()
            count = await session.scalar(select(func.count()).select_from(User))
            assert count == 1

    # @pytest.mark.skip
    @inject
    async def test_create_product(
        self,
        make_session: async_sessionmaker[AsyncSession] = Provide[
            Container.make_session
        ],
    ):
        async with make_session() as session:
            product = Product(name="Test Product", price=100)
            session.add(product)
            await session.commit()
            count = await session.scalar(select(func.count()).select_from(Product))
            assert count == 1

    # @pytest.mark.skip
    @inject
    async def test_create_order(
        self,
        make_session: async_sessionmaker[AsyncSession] = Provide[
            Container.make_session
        ],
    ):
        async with make_session() as session:
            user = User(username="testuser", email="test@example.com")
            product = Product(name="Test Product", price=100)
            session.add_all([user, product])
            await session.commit()
            order = Order(user_id=user.id, product_id=product.id, quantity=2)
            session.add(order)
            await session.commit()
            count = await session.scalar(select(func.count()).select_from(Order))
            assert count == 1

    # @pytest.mark.skip
    @inject
    async def test_create_log(
        self,
        make_session: async_sessionmaker[AsyncSession] = Provide[
            Container.make_session
        ],
    ):
        async with make_session() as session:
            log = Log(
                event="User logged in", details="User testuser logged in successfully"
            )
            session.add(log)
            await session.commit()
            count = await session.scalar(select(func.count()).select_from(Log))
            assert count == 1
