from dependency_injector.wiring import inject, Provide
from fastapi_lab.container import Container
from sqlalchemy import text


@inject
async def on_checking_broker(engine=Provide[Container.engine]):
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))
        return result.scalar_one()
