from typing import List, Optional

from fastapi import Depends

from logicmate_backend.dto.video.video_create_dto import VideoCreate
from logicmate_backend.models.video_model import Video
from logicmate_backend.repositories.video_respository import VideoRepository


class VideoService:
    def __init__(self, repo: VideoRepository = Depends()):
        self.repo: VideoRepository = repo

    def list_videos(self) -> List[Video]:
        return self.repo.list_all()

    def get_video(self, video_id: str) -> Optional[Video]:
        return self.repo.get_by_id(video_id)

    def create_video(self, payload: VideoCreate) -> Video:
        return self.repo.create(payload)

    def update_video(self, video_id: str, data: dict) -> Optional[Video]:
        return self.repo.update(video_id, data)

    def delete_video(self, video_id: str) -> bool:
        return self.repo.delete(video_id)
