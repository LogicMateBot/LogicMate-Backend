from fastapi import APIRouter, Depends, HTTPException, status, Body
from motor.motor_asyncio import AsyncIOMotorDatabase

from logicmate_backend.config.db import get_main_db
from logicmate_backend.dto.token_dto import (
    TokenPayloadDTO,
    TokenRequestDTO,
    TokenResponseDTO,
)
from logicmate_backend.dto.user_dto import UserResponseDTO
from logicmate_backend.repositories.user_repository import UserRepository
from logicmate_backend.services.token_service import TokenService
from logicmate_backend.services.errors import ServiceError
from logicmate_backend.services.user_service import UserService


def get_user_repository(
    db: AsyncIOMotorDatabase = Depends(dependency=get_main_db),
) -> UserRepository:
    return UserRepository(db=db)


def get_token_service(
    repo: UserRepository = Depends(dependency=get_user_repository),
) -> TokenService:
    return TokenService(user_repository=repo)


def get_user_service(
    repo: UserRepository = Depends(dependency=get_user_repository),
) -> UserService:
    return UserService(user_repository=repo)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/login",
    response_model=TokenResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_token(
    payload: TokenRequestDTO,
    auth_service: TokenService = Depends(dependency=get_token_service),
    user_service: UserService = Depends(dependency=get_user_service),
) -> TokenResponseDTO:
    try:
        user_dto: UserResponseDTO | None = await user_service.get_by_email(
            email=payload.email
        )

        if user_dto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return auth_service.create_jwt_token(
            token_payload=TokenPayloadDTO(
                user_id=user_dto.id,
                first_name=user_dto.first_name,
                last_name=user_dto.last_name,
                email=user_dto.email,
            )
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(object=e),
        )
