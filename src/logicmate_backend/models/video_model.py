from typing import List, Optional

from pydantic import BaseModel, Field

from logicmate_backend.models.scene_model import Scene


class Video(BaseModel):
    id: str
    duration: str
    categories: Optional[List[str]] = Field(
        default=None, description="List of categories associated with the video"
    )
    scenes: List[Scene]
    explanation: Optional[str] = Field(
        default=None, description="Explanation of the video"
    )
