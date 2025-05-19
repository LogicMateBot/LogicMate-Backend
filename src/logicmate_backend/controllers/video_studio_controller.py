from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from logicmate_backend.config.database import get_studio_db
from logicmate_backend.dto.video.video_create_dto import VideoCreate
from logicmate_backend.models.video_model import Video
from logicmate_backend.repositories.video_respository import VideoRepository
from logicmate_backend.services.video_service import VideoService
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/studio/videos", tags=["videos-studio"])

def get_video_service(db: AsyncIOMotorDatabase = Depends(get_studio_db)) -> VideoService:
    return VideoService(VideoRepository(db))

@router.get("/", response_model=List[Video])
async def list_videos(service: VideoService = Depends(get_video_service)) -> List[Video]:
    return await service.list_videos()

@router.get("/{video_id}", response_model=Video)
async def get_video(video_id: str, service: VideoService = Depends(get_video_service)) -> Video:
    video = await service.get_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.post("/", response_model=Video, status_code=status.HTTP_201_CREATED)
async def create_video(payload: VideoCreate, service: VideoService = Depends(get_video_service)) -> Video:
    return await service.create_video(payload)

@router.put("/{video_id}", response_model=Video)
async def update_video(video_id: str, data: Dict[str, Any], service: VideoService = Depends(get_video_service)) -> Video:
    updated = await service.update_video(video_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Video not found")
    return updated

@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(video_id: str, service: VideoService = Depends(get_video_service)) -> None:
    success = await service.delete_video(video_id)
    if not success:
        raise HTTPException(status_code=404, detail="Video not found")
