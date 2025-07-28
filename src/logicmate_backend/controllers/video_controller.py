from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
import json
from motor.motor_asyncio import AsyncIOMotorDatabase


from logicmate_backend.config.db import get_main_db
from logicmate_backend.dto.video_dto import (
    VideoRequestDTO,
    VideoResponseDTO,
    ProcessVideoRequestDTO,
)
from logicmate_backend.repositories.video_repository import VideoRepository
from logicmate_backend.services.video_service import VideoService
from logicmate_backend.services.errors import ServiceError
from logicmate_backend.utils.celery import celery


def get_video_repository(
    db: AsyncIOMotorDatabase = Depends(dependency=get_main_db),
) -> VideoRepository:
    return VideoRepository(db=db)


def get_video_service(
    repo: VideoRepository = Depends(dependency=get_video_repository),
) -> VideoService:
    return VideoService(video_repository=repo)


router = APIRouter(prefix="/api/v1/videos", tags=["videos"])


@router.get(path="/", response_model=List[VideoResponseDTO])
async def list_videos(
    service: VideoService = Depends(dependency=get_video_service),
) -> List[VideoResponseDTO]:
    try:
        videos: List[VideoResponseDTO] = await service.get_all()
        return videos
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(object=e)
        )


@router.get(path="/{video_id}", response_model=VideoResponseDTO)
async def get_video(
    video_id: str, service: VideoService = Depends(dependency=get_video_service)
) -> VideoResponseDTO:
    try:
        video: VideoResponseDTO | None = await service.get_by_id(video_id=video_id)
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(object=e)
        )

    if video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )

    return video


@router.post(path="/process")
async def process_videos(
    file: UploadFile = File(default=...),
    users_emails: str = Form(default=...),
    current_user_email: str = Form(default=...),
) -> dict[str, str]:
    try:
        parsed_users_emails = json.loads(users_emails)
        request_dto = ProcessVideoRequestDTO(
            file=file,
            users_emails=parsed_users_emails,
            current_user_email=current_user_email,
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON format for usersEmails",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(object=e)}",
        )

    if request_dto.file.content_type != "video/mp4":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only MP4 video files are supported",
        )

    data: bytes = await request_dto.file.read()

    result = celery.send_task(
        name="logicmate_bot.process_video",
        args=[data, request_dto.users_emails, request_dto.current_user_email],
    )

    return {"message": "Video enqueued for bot processing", "task_id": result.id}


@router.post(
    path="/", response_model=VideoResponseDTO, status_code=status.HTTP_201_CREATED
)
async def create_video(
    payload: VideoRequestDTO,
    service: VideoService = Depends(dependency=get_video_service),
) -> VideoResponseDTO:
    try:
        created: VideoResponseDTO | None = await service.create(video_dto=payload)
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(object=e)
        )

    if created is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Video creation failed"
        )

    return created


@router.get(path="/by-user/", response_model=List[VideoResponseDTO])
async def get_videos_by_user(
    email: str,
    service: VideoService = Depends(dependency=get_video_service),
) -> List[VideoResponseDTO]:
    try:
        videos: List[VideoResponseDTO] = await service.get_all_by_user_email(
            user_email=email
        )
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch videos for user {email}: {str(object=e)}",
        )

    return videos
