from typing import List, Optional
from pydantic import BaseModel, Field
from logicmate_backend.models.scene_model import Scene
from bson import ObjectId


class Video(BaseModel):
    id: Optional[str] = Field(alias="_id")
    duration: str
    categories: Optional[List[str]] = Field(
        default=None, description="List of categories associated with the video"
    )
    scenes: List[Scene]
    explanation: Optional[str] = Field(
        default=None, description="Explanation of the video"
    )

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
