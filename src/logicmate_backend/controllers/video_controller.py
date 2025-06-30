from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from logicmate_backend.config.db import get_main_db
from logicmate_backend.dto.video_dto import VideoRequestDTO, VideoResponseDTO
from logicmate_backend.repositories.video_repository import VideoRepository
from logicmate_backend.services.video_service import VideoService
from logicmate_backend.services.errors import ServiceError


def get_video_repository(
    db: AsyncIOMotorDatabase = Depends(dependency=get_main_db),
) -> VideoRepository:
    return VideoRepository(db=db)


def get_video_service(
    repo: VideoRepository = Depends(dependency=get_video_repository),
) -> VideoService:
    return VideoService(video_repository=repo)


router = APIRouter(prefix="/videos", tags=["videos"])


@router.get(path="/", response_model=List[VideoResponseDTO])
async def list_videos(
    service: VideoService = Depends(dependency=get_video_service),
) -> List[VideoResponseDTO]:
    try:
        videos = await service.get_all()
        return videos
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(path="/{video_id}", response_model=VideoResponseDTO)
async def get_video(
    video_id: str, service: VideoService = Depends(dependency=get_video_service)
) -> VideoResponseDTO:
    try:
        video = await service.get_by_id(video_id=video_id)
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    if video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )

    return video


@router.post(
    path="/", response_model=VideoResponseDTO, status_code=status.HTTP_201_CREATED
)
async def create_video(
    payload: VideoRequestDTO,
    service: VideoService = Depends(dependency=get_video_service),
) -> VideoResponseDTO:
    try:
        created = await service.create(video_dto=payload)
    except ServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if created is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Video creation failed"
        )

    return created


@router.put(path="/{video_id}", response_model=VideoResponseDTO)
async def update_video(
    video_id: str,
    payload: VideoRequestDTO,
    service: VideoService = Depends(dependency=get_video_service),
) -> VideoResponseDTO:
    try:
        updated = await service.update(video_id=video_id, video_dto=payload)
    except ServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found for update"
        )

    return updated


@router.delete(path="/{video_id}", response_model=VideoResponseDTO)
async def delete_video(
    video_id: str, service: VideoService = Depends(dependency=get_video_service)
) -> VideoResponseDTO:
    try:
        deleted = await service.delete(video_id=video_id)
    except ServiceError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found for deletion"
        )

    return deleted
