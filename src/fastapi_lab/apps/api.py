from fastapi import APIRouter
from fastapi_lab.modules.system_maintaining.presentation.http.on_checking_liveness import (
    on_checking_liveness,
)
from fastapi_lab.modules.system_maintaining.presentation.http.on_checking_readiness import (
    on_checking_readiness,
)
from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import Optional, TypedDict, cast
from fastapi import FastAPI
from fastapi_lab.container import Container, packages
from fastapi_lab.apps.worker import app as celery_app
from inspect import isawaitable


class State(TypedDict):
    container: Container


@asynccontextmanager
async def lifespan(fastapi_app: Optional[FastAPI] = None):
    container = Container()
    container.wire(
        packages=packages(),
    )
    with celery_app.connection() as connection:
        connection.ensure_connection(max_retries=3)
    yield cast(State, {"container": container})
    if isawaitable(awaitable := container.shutdown_resources()):
        await awaitable
    if engine := container.engine():
        await engine.dispose()


router = APIRouter()
router.add_api_route(path="/liveness", endpoint=on_checking_liveness, methods=["GET"])
router.add_api_route(path="/readiness", endpoint=on_checking_readiness, methods=["GET"])
app = FastAPI(lifespan=lifespan)
app.include_router(router)
