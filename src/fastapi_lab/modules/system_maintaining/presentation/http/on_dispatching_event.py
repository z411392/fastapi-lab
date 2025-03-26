from dependency_injector.wiring import inject
from fastapi_lab.schemas.response_payload import ResponsePayload


@inject
async def on_dispatching_event():
    return ResponsePayload()
