from typing import List
from bson import ObjectId
from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, Field, field_validator
from logicmate_backend.models.video import Scene


class VideoRequestDTO(BaseModel):
    id: str
    duration: str
    categories: List[str]
    scenes: List[Scene]
    title: str
    explanation: str
    code: str
    diagram: str
    approaches: List
    exercises: List
    users: List


class VideoResponseDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=False)

    id: str = Field(alias="_id")
    duration: str
    categories: List[str]
    scenes: List
    title: str
    explanation: str
    code: str
    diagram: str
    approaches: List
    exercises: List
    users: List

    @field_validator("id", mode="before")
    @classmethod
    def _convert_object_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v


class ProcessVideoRequestDTO(BaseModel):
    file: UploadFile = Field(default=..., description="MP4 video file to process")
    users_emails: List[str] = Field(
        default=..., description="List of user emails to notify"
    )
    current_user_email: str = Field(
        default=..., description="Email of the current user"
    )

    class Config:
        arbitrary_types_allowed = True
