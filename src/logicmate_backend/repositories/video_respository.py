from typing import Any, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from logicmate_backend.dto.video.video_create_dto import VideoCreate
from logicmate_backend.models.video_model import Video


def transform_id(data: dict) -> dict:
    if not data:
        return data
    data["id"] = str(data["_id"])
    del data["_id"]
    return data

class VideoRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db["videos"]

    async def list_all(self) -> List[Video]:
        cursor = self.collection.find({})
        videos = await cursor.to_list(length=100)
        return [Video(**transform_id(v)) for v in videos]

    async def get_by_id(self, video_id: str) -> Optional[Video]:
        data = await self.collection.find_one({"_id": ObjectId(video_id)})
        return Video(**transform_id(data)) if data else None

    async def create(self, video: VideoCreate) -> Video:
        payload = video.model_dump()
        result = await self.collection.insert_one(payload)
        created = await self.collection.find_one({"_id": result.inserted_id})
        created = transform_id(created)
        return Video(**created)

    async def update(self, video_id: str, data: dict) -> Optional[Video]:
        await self.collection.update_one({"_id": ObjectId(video_id)}, {"$set": data})
        updated = await self.collection.find_one({"_id": ObjectId(video_id)})
        return Video(**transform_id(updated)) if updated else None

    async def delete(self, video_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(video_id)})
        return result.deleted_count == 1
