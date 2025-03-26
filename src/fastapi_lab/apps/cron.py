from celery.schedules import crontab
from fastapi_lab.apps.worker import app

app.conf.beat_schedule = {
    "check_broker": {
        "task": "check_broker",
        "schedule": crontab(minute="*"),
        # "args": (1, 2),
    },
}
