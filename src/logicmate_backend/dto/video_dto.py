from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator
from logicmate_backend.models.video import Scene


class VideoRequestDTO(BaseModel):
    duration: str
    categories: Optional[List[str]] = Field(default=None)
    scenes: List[Scene]
    explanation: Optional[str] = Field(default=None)


class VideoResponseDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=False)

    id: Optional[str] = Field(alias="_id")
    duration: str
    categories: Optional[List[str]] = Field(default=None)
    scenes: List[Scene]
    explanation: Optional[str] = Field(default=None)

    @field_validator("id", mode="before")
    @classmethod
    def _convert_object_id(cls, v):
        if isinstance(v, ObjectId):
            return str(object=v)
        return v
