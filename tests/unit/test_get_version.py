import pytest
from fastapi_lab.container import Container, packages
from dependency_injector.wiring import inject, Provide


@pytest.mark.skip
class TestGetVersion:
    @pytest.fixture(autouse=True)
    async def container(self):
        container = Container()
        container.wire(
            packages=packages(),
        )
        container.wire(modules=[__name__])
        yield container
        container.unwire()

    @inject
    @pytest.mark.describe("要能夠執行 unit test")
    async def test_get_version(self, version: str = Provide[Container.version]):
        assert version == "0.1.0"
