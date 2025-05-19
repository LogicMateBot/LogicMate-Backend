from typing import Any, List, Optional
from logicmate_backend.dto.video.video_create_dto import VideoCreate
from logicmate_backend.models.video_model import Video


class VideoRepository:
    def __init__(self):
        self._storage: List[Video] = []

    def list_all(self) -> List[Video]:
        return self._storage

    def get_by_id(self, video_id: str) -> Optional[Video]:
        return next((v for v in self._storage if v.id == video_id), None)

    def create(self, video: VideoCreate) -> Video:
        new_id = str(object=len(self._storage) + 1)

        payload: dict[str, Any] = video.model_dump()
        payload["id"] = new_id

        new_video = Video(**payload)
        self._storage.append(new_video)
        return new_video

    def update(self, video_id: str, data: dict) -> Optional[Video]:
        existing = self.get_by_id(video_id)
        if not existing:
            return None

        updated: Video = existing.model_copy(update=data)
        idx: int = self._storage.index(existing)
        self._storage[idx] = updated
        return updated

    def delete(self, video_id: str) -> bool:
        existing: Video | None = self.get_by_id(video_id)
        if not existing:
            return False
        self._storage.remove(existing)
        return True
