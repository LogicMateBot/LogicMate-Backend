from typing import List, Optional
from pydantic import BaseModel, Field
from logicmate_backend.models.video import Scene


class VideoRequestDTO(BaseModel):
    duration: str
    categories: Optional[List[str]] = Field(default=None)
    scenes: List[Scene]
    explanation: Optional[str] = Field(default=None)


class VideoResponseDTO(BaseModel):
    id: Optional[str] = Field(alias="_id")
    duration: str
    categories: Optional[List[str]] = Field(default=None)
    scenes: List[Scene]
    explanation: Optional[str] = Field(default=None)
