import pytest
from os import getenv

pytest_plugins = ("celery.contrib.pytest",)


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": getenv("BROKER_URL"),
        "result_backend": "rpc://",
        "timezone": getenv("TZ"),
        "accept_content": ("json", "pickle"),
    }