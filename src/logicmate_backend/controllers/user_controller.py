from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from logicmate_backend.config.db import get_main_db
from logicmate_backend.dto.user_dto import UserRequestDTO, UserResponseDTO
from logicmate_backend.repositories.user_repository import UserRepository
from logicmate_backend.services.user_service import UserService
from logicmate_backend.services.errors import ServiceError


def get_user_repository(
    db: AsyncIOMotorDatabase = Depends(dependency=get_main_db),
) -> UserRepository:
    return UserRepository(db=db)


def get_user_service(
    repo: UserRepository = Depends(dependency=get_user_repository),
) -> UserService:
    return UserService(user_repository=repo)


router = APIRouter(prefix="/users", tags=["users"])


@router.get(path="/", response_model=List[UserResponseDTO])
async def list_users(
    service: UserService = Depends(dependency=get_user_service),
) -> List[UserResponseDTO]:
    try:
        users_dto: List[UserResponseDTO] = await service.get_all()

        return users_dto
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(object=e)
        )


@router.get(path="/{user_id}", response_model=Optional[UserResponseDTO])
async def get_user(
    user_id: str, service: UserService = Depends(dependency=get_user_service)
) -> Optional[UserResponseDTO]:
    try:
        user_dto: UserResponseDTO | None = await service.get_by_id(user_id=user_id)
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(object=e)
        )

    if user_dto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user_dto


@router.post(
    path="/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED
)
async def create_user(
    payload: UserRequestDTO, service: UserService = Depends(dependency=get_user_service)
) -> UserResponseDTO:
    try:
        created_user_dto: UserResponseDTO | None = await service.create(
            user_dto=payload
        )
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(object=e)
        )

    if created_user_dto is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User creation failed"
        )

    return created_user_dto


@router.put(path="/{user_id}", response_model=UserResponseDTO)
async def update_user(
    user_id: str,
    payload: UserRequestDTO,
    service: UserService = Depends(dependency=get_user_service),
) -> UserResponseDTO:
    try:
        updated_user_dto: UserResponseDTO | None = await service.update(
            user_id=user_id, user_dto=payload
        )
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(object=e)
        )

    if updated_user_dto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found for update"
        )

    return updated_user_dto


@router.delete(path="/{user_id}", response_model=UserResponseDTO)
async def delete_user(
    user_id: str, service: UserService = Depends(dependency=get_user_service)
) -> UserResponseDTO:
    try:
        deleted_user_dto: UserResponseDTO | None = await service.delete(user_id=user_id)
    except ServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(object=e)
        )

    if deleted_user_dto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found for deletion"
        )

    return deleted_user_dto
