from celery import Celery
import time

celery_app = Celery(
    "logicmate",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task(name="logicmate_backend.celery_app.process_videos_celery")
def process_videos_celery(video_path: str):
    
    print(f"Procesando video: {video_path}")
    time.sleep(20)
    return f"Video {video_path} procesado"
