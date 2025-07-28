import os
from celery import Celery

celery = Celery(
    main="logicmate_backend",
    broker=os.getenv(key="CELERY_BROKER_URL", default="redis://localhost:6379/0"),
    backend=os.getenv(key="CELERY_RESULT_BACKEND", default="redis://localhost:6379/1"),
)
