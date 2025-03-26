from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI
from fastapi_lab.container import Container


@asynccontextmanager
async def lifespan(app: Optional[FastAPI] = None):
    container = Container()
    container.wire()
    await container.init_resources()
    yield container
    await container.shutdown_resources()
