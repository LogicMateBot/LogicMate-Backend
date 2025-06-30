from pydantic import BaseModel


class TokenRequestDTO(BaseModel):
    email: str
    password: str


class TokenPayloadDTO(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str


class TokenResponseDTO(BaseModel):
    access_token: str
