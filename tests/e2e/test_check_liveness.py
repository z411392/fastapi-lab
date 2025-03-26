import pytest
from httpx import ASGITransport, AsyncClient
from fastapi_lab.apps.api import app


class TestSystemMaintainingEndpoints:
    @pytest.mark.asyncio
    @pytest.mark.describe("要能夠執行 e2e test")
    async def test_check_liveness(self):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/liveness")
            assert response.status_code == 200
            assert response.json() == {"message": "OK"}
