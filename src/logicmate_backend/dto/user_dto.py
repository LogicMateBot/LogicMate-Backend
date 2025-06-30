from bson import ObjectId
from pydantic import BaseModel, ConfigDict, field_validator


class UserRequestDTO(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: str
    password: str


class UserResponseDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=False)

    id: str
    email: str
    first_name: str
    last_name: str
    username: str

    @field_validator("id", mode="before")
    @classmethod
    def _convert_object_id(cls, v):
        if isinstance(v, ObjectId):
            return str(object=v)
        return v
