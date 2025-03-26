from fastapi import APIRouter
from fastapi_lab.modules.system_maintaining.presentation.http.on_dispatching_event import (
    on_dispatching_event,
)
from fastapi import FastAPI
from fastapi_lab.lifespan import lifespan

router = APIRouter()
router.add_api_route(path="/", endpoint=on_dispatching_event, methods=["POST"])
app = FastAPI(lifespan=lifespan)
app.include_router(router)
