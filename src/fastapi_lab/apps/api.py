from fastapi import APIRouter
from fastapi_lab.modules.system_maintaining.presentation.on_checking_liveness import (
    on_checking_liveness,
)
from fastapi import FastAPI
from fastapi_lab.lifespan import lifespan

router = APIRouter()
router.add_api_route(path="/liveness", endpoint=on_checking_liveness, methods=["GET"])
app = FastAPI(lifespan=lifespan)
app.include_router(router)
