from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from fastapi_lab.container import Container
from typing import Annotated
from fastapi_lab.schemas.response_payload import ResponsePayload
from pydantic import BaseModel


class LivenessResponse(BaseModel):
    version: str


@inject
async def on_checking_liveness(
    version: Annotated[str, Depends(Provide[Container.version])],
):
    return ResponsePayload(
        data=LivenessResponse(version=version),
    )
