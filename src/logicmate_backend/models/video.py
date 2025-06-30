from typing import List, Optional
from pydantic import BaseModel, Field

from logicmate_backend.models.common import PyObjectId


class Prediction(BaseModel):
    x: float
    y: float
    width: float
    height: float
    text: Optional[str] = Field(
        default=None, description="Text associated with the prediction"
    )
    explanation: Optional[str] = Field(
        default=None, description="Explanation of the prediction"
    )
    class_name: Optional[str] = Field(
        default=None,
        description="Class name of the prediction. This is used for classification tasks.",
    )


class Image(BaseModel):
    path: str
    categories: Optional[List[str]] = Field(
        default=None, description="Category of the image"
    )
    explanation: Optional[str] = Field(
        default=None, description="Explanation of the image"
    )
    predictions: Optional[List[Prediction]] = Field(
        default=None, description="List of predictions associated with the image"
    )


class Scene(BaseModel):
    scene_id: int
    start_timestamp: str
    end_timestamp: str
    categories: Optional[List[str]] = Field(
        default=None, description="Category of the scene"
    )
    images: List[Image]
    explanation: Optional[str] = Field(
        default=None, description="Explanation of the scene"
    )


class Video(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
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
        json_encoders = {PyObjectId: str}
