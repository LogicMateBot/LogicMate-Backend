from typing import List, Optional

from pydantic import BaseModel, Field

from logicmate_backend.models.prediction_model import PredictionBase


class ImageModel(BaseModel):
    path: str
    categories: Optional[List[str]] = Field(
        default=None, description="Category of the image"
    )
    explanation: Optional[str] = Field(
        default=None, description="Explanation of the image"
    )
    predictions: Optional[List[PredictionBase]] = Field(
        default=None, description="List of predictions associated with the image"
    )
