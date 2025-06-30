from typing import Any, Optional
from logicmate_backend.dto.user_dto import UserRequestDTO, UserResponseDTO
from logicmate_backend.models.user import User
from logicmate_backend.repositories.errors import RepositoryError
from logicmate_backend.repositories.user_repository import UserRepository
from logicmate_backend.services.errors import ServiceError
from logicmate_backend.utils.security import hash_password


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository: UserRepository = user_repository

    async def get_all(self) -> list[UserResponseDTO]:
        try:
            users: list[User] = await self.user_repository.get_all()
        except RepositoryError as e:
            raise ServiceError(f"Error retrieving users: {e}")

        users_dto: list[UserResponseDTO] = [
            UserResponseDTO.model_validate(obj=user.__dict__) for user in users
        ]

        return users_dto

    async def get_by_id(self, user_id: str) -> Optional[UserResponseDTO]:
        try:
            user: User | None = await self.user_repository.get_by_id(user_id=user_id)
        except RepositoryError as e:
            raise ServiceError(f"Error retrieving user by ID: {e}")

        if user is None:
            return None

        return UserResponseDTO.model_validate(obj=user.__dict__)

    async def get_by_email(self, email: str) -> Optional[UserResponseDTO]:
        try:
            user: User | None = await self.user_repository.get_by_email(email=email)
        except RepositoryError as e:
            raise ServiceError(f"Error retrieving user by email: {e}")

        if user is None:
            return None

        return UserResponseDTO.model_validate(obj=user.__dict__)

    async def create(self, user_dto: UserRequestDTO) -> Optional[UserResponseDTO]:
        user_dict: dict[str, Any] = user_dto.model_dump()
        user_dict["password"] = hash_password(password=user_dict.get("password", ""))

        try:
            created_user: User | None = await self.user_repository.create(
                user_dict=user_dict
            )
        except RepositoryError as e:
            raise ServiceError(f"Error creating user: {e}")

        if created_user is None:
            return None

        return UserResponseDTO.model_validate(obj=created_user.__dict__)

    async def update(
        self, user_id: str, user_dto: UserRequestDTO
    ) -> Optional[UserResponseDTO]:
        user_dict: dict[str, Any] = user_dto.model_dump()

        try:
            updated_user: User | None = await self.user_repository.update(
                user_id=user_id, user_dict=user_dict
            )
        except RepositoryError as e:
            raise ServiceError(f"Error updating user: {e}")

        if updated_user is None:
            return None

        return UserResponseDTO.model_validate(obj=updated_user.__dict__)

    async def delete(self, user_id: str) -> Optional[UserResponseDTO]:
        try:
            deleted_user: User | None = await self.user_repository.delete(
                user_id=user_id
            )
        except RepositoryError as e:
            raise ServiceError(f"Error deleting user: {e}")

        if deleted_user is None:
            return None

        return UserResponseDTO.model_validate(obj=deleted_user.__dict__)
