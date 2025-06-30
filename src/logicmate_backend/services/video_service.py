from typing import Any, Dict, Optional, List

from logicmate_backend.dto.video_dto import VideoRequestDTO, VideoResponseDTO
from logicmate_backend.models.video import Video
from logicmate_backend.repositories.video_repository import VideoRepository
from logicmate_backend.repositories.errors import RepositoryError
from logicmate_backend.services.errors import ServiceError


class VideoService:
    def __init__(self, video_repository: VideoRepository) -> None:
        self.video_repository: VideoRepository = video_repository

    async def get_all(self) -> List[VideoResponseDTO]:
        try:
            videos: List[Video] = await self.video_repository.get_all()
        except RepositoryError as e:
            raise ServiceError(f"Error retrieving videos: {e}")

        return [VideoResponseDTO.model_validate(obj=video.__dict__) for video in videos]

    async def get_by_id(self, video_id: str) -> Optional[VideoResponseDTO]:
        try:
            video: Optional[Video] = await self.video_repository.get_by_id(
                video_id=video_id
            )
        except RepositoryError as e:
            raise ServiceError(f"Error retrieving video by ID: {e}")

        if video is None:
            return None

        return VideoResponseDTO.model_validate(obj=video.__dict__)

    async def create(self, video_dto: VideoRequestDTO) -> Optional[VideoResponseDTO]:
        video_dict: Dict[str, Any] = video_dto.model_dump()

        try:
            created_video: Optional[Video] = await self.video_repository.create(
                video_dict=video_dict
            )
        except RepositoryError as e:
            raise ServiceError(f"Error creating video: {e}")

        if created_video is None:
            return None

        return VideoResponseDTO.model_validate(obj=created_video.__dict__)
