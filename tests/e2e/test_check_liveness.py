import pytest
from httpx import ASGITransport, AsyncClient
from fastapi_lab.apps.api import app
from typing import cast
from fastapi_lab.container import Container


@pytest.mark.skip
class TestCheckLivness:
    @pytest.mark.describe("要能夠檢查 liveness")
    async def test_check_liveness(self):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            async with app.router.lifespan_context(app) as state:
                container = cast(Container, state.get("container"))
                response = await client.get("/liveness")
                assert response.status_code == 200
                payload = response.json()
                assert "data" in payload
                data = payload["data"]
                assert "version" in data
                assert data["version"] == container.version()
