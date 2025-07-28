from typing import List
from pydantic import BaseModel

from logicmate_backend.models.common import PyObjectId


class Video(BaseModel):
    id: str
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

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
