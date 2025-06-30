from typing import List, Optional
from pydantic import BaseModel, Field

from logicmate_backend.models.common import PyObjectId


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    is_active: bool = True
    videos: List[PyObjectId] = []

    class Config:
        json_encoders = {PyObjectId: str}
        validate_by_name = True
        arbitrary_types_allowed = True
        validate_assignment = True
        use_enum_values = True
