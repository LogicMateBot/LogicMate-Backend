from typing import List, Optional

from pydantic import BaseModel, Field

from logicmate_backend.models.image_model import ImageModel


class Scene(BaseModel):
    scene_id: int
    start_timestamp: str
    end_timestamp: str
    categories: Optional[List[str]] = Field(
        default=None, description="Category of the scene"
    )
    images: List[ImageModel]
    explanation: Optional[str] = Field(
        default=None, description="Explanation of the scene"
    )
