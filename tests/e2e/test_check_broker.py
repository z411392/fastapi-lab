import pytest
from pytest_celery import CeleryTestWorker
from fastapi_lab.apps.worker import check_broker


@pytest.mark.skip
class TestCheckBroker:
    @pytest.mark.describe("要能夠檢查 broker")
    def test_check_broker(self, celery_worker: CeleryTestWorker):
        assert check_broker.delay().get(timeout=5) == 1
