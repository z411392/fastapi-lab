from celery import Celery, Task
from asyncio import run, wait
from os import getenv
from typing import cast, Callable
from fastapi_lab.container import Container, packages
from inspect import isawaitable
from fastapi_lab.modules.system_maintaining.presentation.amqp.on_checking_broker import (
    on_checking_broker,
)


class ContextTask(Task):
    def __call__(self, *args, **kwargs):
        container = Container()
        container.wire(
            packages=packages(),
        )
        try:
            return run(self.run(*args, **kwargs))
        finally:
            if isawaitable(awaitable := container.shutdown_resources()):
                wait(awaitable)
            if engine := container.engine():
                wait(engine.dispose())


app = Celery(
    "app",
    broker=getenv("BROKER_URL"),
    backend="rpc://",
    timezone=getenv("TZ"),
)


def register_task(name: str, handler: Callable) -> Task:
    return cast(Task, app.task(name=name, base=ContextTask)(handler))


check_broker = register_task("check_broker", on_checking_broker)
