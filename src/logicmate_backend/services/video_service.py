from typing import List, Optional

from logicmate_backend.dto.video.video_create_dto import VideoCreate
from logicmate_backend.models.video_model import Video
from logicmate_backend.repositories.video_respository import VideoRepository


class VideoService:
    def __init__(self, repo: VideoRepository):
        self.repo = repo

    async def list_videos(self) -> List[Video]:
        return await self.repo.list_all()

    async def get_video(self, video_id: str) -> Optional[Video]:
        return await self.repo.get_by_id(video_id)

    async def create_video(self, payload: VideoCreate) -> Video:
        return await self.repo.create(payload)

    async def update_video(self, video_id: str, data: dict) -> Optional[Video]:
        return await self.repo.update(video_id, data)

    async def delete_video(self, video_id: str) -> bool:
        return await self.repo.delete(video_id)
