from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from fastapi_lab.container import Container
from typing import Annotated
from fastapi_lab.schemas.response_payload import ResponsePayload
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text


class ReadinessResponse(BaseModel):
    version: str


@inject
async def on_checking_readiness(
    engine: Annotated[AsyncEngine, Depends(Provide[Container.engine])],
):
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
    return ResponsePayload(
        data=ReadinessResponse(),
    )
