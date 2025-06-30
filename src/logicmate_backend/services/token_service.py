import os
import jwt
from typing import Any
from datetime import datetime, timedelta, timezone
from logicmate_backend.dto.token_dto import TokenPayloadDTO, TokenResponseDTO
from logicmate_backend.models.token import TokenPayload
from logicmate_backend.models.user import User
from logicmate_backend.repositories.user_repository import UserRepository


class TokenService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository: UserRepository = user_repository
        self.ACCESS_TOKEN_SECRET_KEY: str | None = os.environ.get(
            "ACCESS_TOKEN_SECRET_KEY"
        )
        self.ACCESS_TOKEN_EXPIRATION_TIME_MINUTES = int(
            os.environ.get("ACCESS_TOKEN_EXPIRATION_TIME_MINUTES", default=60)
        )

    def create_jwt_token(self, token_payload: TokenPayloadDTO) -> TokenResponseDTO:
        payload_dto: dict[str, Any] = token_payload.model_dump()
        now: datetime = datetime.now(tz=timezone.utc)
        exp: datetime = now + timedelta(
            minutes=self.ACCESS_TOKEN_EXPIRATION_TIME_MINUTES
        )

        payload = TokenPayload(
            user_id=payload_dto["user_id"],
            first_name=payload_dto["first_name"],
            last_name=payload_dto["last_name"],
            email=payload_dto["email"],
            exp=int(exp.timestamp()),
            iat=int(now.timestamp()),
        )

        try:
            encoded_jwt: str = jwt.encode(
                payload=payload.model_dump(),
                key=self.ACCESS_TOKEN_SECRET_KEY,
                algorithm="HS256",
            )
        except jwt.PyJWTError as e:
            raise RuntimeError("Error creating JWT token") from e
        except Exception as e:
            raise RuntimeError("Unexpected error creating JWT token") from e

        return TokenResponseDTO(
            access_token=encoded_jwt,
        )

    async def decode_jwt_token(self, token: str) -> User:
        try:
            payload: dict[str, Any] = jwt.decode(
                jwt=token,
                key=self.ACCESS_TOKEN_SECRET_KEY,
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

        user_id: str | None = payload.get("user_id")
        if not user_id:
            raise ValueError("Token does not contain user_id")

        user: User | None = await self.user_repository.get_by_id(
            user_id=str(object=user_id)
        )
        if not user:
            raise ValueError("User not found")

        return user
