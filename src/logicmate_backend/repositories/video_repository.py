from typing import Any, Dict, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError
from pymongo.results import InsertOneResult

from logicmate_backend.models.video import Video
from logicmate_backend.repositories.errors import RepositoryError


class VideoRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
        self.collection = self.db["videos"]

    def _validate_video_id(self, video_id: str) -> ObjectId:
        try:
            return ObjectId(oid=video_id)
        except Exception as e:
            raise RepositoryError(f"Invalid video ID format: {video_id}") from e

    async def get_all(self) -> List[Video]:
        try:
            cursor = self.collection.find({})
            videos_json: List[Dict[str, Any]] = await cursor.to_list(length=100)
        except PyMongoError as e:
            raise RepositoryError(f"Error retrieving videos from MongoDB: {e}")

        return [Video(**video) for video in videos_json]

    async def get_by_id(self, video_id: str) -> Optional[Video]:
        _id: ObjectId = self._validate_video_id(video_id=video_id)
        try:
            doc = await self.collection.find_one({"_id": _id})
        except PyMongoError as e:
            raise RepositoryError(f"Error retrieving video by ID from MongoDB: {e}")

        if not doc:
            return None
        return Video(**doc)

    async def create(self, video_dict: Dict[str, Any]) -> Video:
        try:
            result: InsertOneResult = await self.collection.insert_one(
                document=video_dict
            )
        except PyMongoError as e:
            raise RepositoryError(f"Error creating video in MongoDB: {e}")

        created: Video | None = await self.get_by_id(video_id=str(result.inserted_id))
        if not created:
            raise RepositoryError("Video creation failed, not found after insertion.")
        return created
