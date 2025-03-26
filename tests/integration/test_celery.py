import pytest
from pytest_celery import CeleryTestWorker
from celery import Celery, Task


@pytest.mark.skip
class TestCelery:
    @pytest.fixture
    def task(self, celery_session_app: Celery):
        def add(x, y):
            return x + y

        return celery_session_app.task(add)

    @pytest.mark.describe("要能夠新增 task")
    def test_create_task(self, task: Task, celery_worker: CeleryTestWorker):
        """
        1. celery_worker 參數必須宣告，celery_worker 才會初始化(function scope)。
        2. celery_worker 必須擺在 task 之後，worker 才會載入得到先前用 celery_session_app 註冊的 task。
        3. 單元測試時的 fixture 變數名稱必須和宣告時相同，否則會無法載入 fixture。
        """
        assert task.delay(1, 2).get(timeout=5) == 3
