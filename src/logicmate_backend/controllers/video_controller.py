from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from logicmate_backend.dto.video.video_create_dto import VideoCreate
from logicmate_backend.models.video_model import Video
from logicmate_backend.services.video_service import VideoService

router = APIRouter(prefix="/videos", tags=["videos"])


@router.get(path="/", response_model=List[Video])
async def list_videos(
    service: VideoService = Depends(),
) -> List[Video]:
    return service.list_videos()


@router.get(path="/{video_id}", response_model=Video)
async def get_video(
    video_id: str,
    service: VideoService = Depends(dependency=VideoService),
) -> Video:
    video: Video | None = service.get_video(video_id=video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )
    return video


@router.post(path="/", response_model=Video, status_code=status.HTTP_201_CREATED)
async def create_video(
    payload: VideoCreate,
    service: VideoService = Depends(dependency=VideoService),
) -> Video:
    return service.create_video(payload=payload)


@router.put(path="/{video_id}", response_model=Video)
async def update_video(
    video_id: str,
    data: Dict[str, Any],
    service: VideoService = Depends(dependency=VideoService),
) -> Video:
    updated: Video | None = service.update_video(video_id=video_id, data=data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )
    return updated


@router.delete(path="/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(
    video_id: str,
    service: VideoService = Depends(dependency=VideoService),
) -> None:
    success: bool = service.delete_video(video_id=video_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )
    return
