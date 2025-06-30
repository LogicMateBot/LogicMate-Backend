from pydantic import BaseModel


class TokenPayload(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str
    exp: int
    iat: int
