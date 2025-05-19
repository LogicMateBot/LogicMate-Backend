from typing import List, Optional
from pydantic import BaseModel, Field
from logicmate_backend.models.scene_model import Scene


class VideoCreate(BaseModel):
    duration: str
    categories: Optional[List[str]] = Field(default=None)
    scenes: List[Scene]
    explanation: Optional[str] = Field(default=None)
