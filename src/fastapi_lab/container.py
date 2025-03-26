from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from os import getenv
from glob import glob
from pathlib import Path
from os.path import dirname, abspath, join
from asyncio import get_event_loop_policy


class Container(containers.DeclarativeContainer):
    version = providers.Object("0.1.0")
    engine = providers.Singleton(
        create_async_engine,
        f"postgresql+asyncpg://{getenv('POSTGRES_DATABASE_USER')}:{getenv('POSTGRES_DATABASE_PASSWORD')}@{getenv('POSTGRES_DATABASE_HOST')}:{getenv('POSTGRES_DATABASE_PORT')}/{getenv('POSTGRES_DATABASE_NAME')}",
        pool_size=5,
        max_overflow=10,
    )
    make_session = providers.Singleton(
        async_sessionmaker,
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


def packages():
    script_dir = dirname(abspath(__file__))
    dir_paths = [
        *glob(join(script_dir, "modules", "*", "presentation", "*")),
        *glob(join(script_dir, "orm", "models", "*")),
    ]
    return [
        "fastapi_lab." + ".".join(Path(dir_path).relative_to(script_dir).parts)
        for dir_path in dir_paths
    ]


container = Container()
container.wire(
    packages=packages(),
)
