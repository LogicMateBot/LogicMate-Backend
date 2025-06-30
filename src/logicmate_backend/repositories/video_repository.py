from typing import Any, Dict, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError, DuplicateKeyError
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
        _id = self._validate_video_id(video_id=video_id)
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

    async def update(self, video_id: str, video_dict: Dict[str, Any]) -> Video:
        _id: ObjectId = self._validate_video_id(video_id=video_id)
        try:
            updated_doc = await self.collection.find_one_and_update(
                filter={"_id": _id},
                update={"$set": video_dict},
                return_document=ReturnDocument.AFTER,
            )
        except DuplicateKeyError as e:
            details: Any | Dict[Any, Any] = getattr(e, "details", {}) or {}
            key_pattern = details.get("keyPattern", {})
            msg = "A video with this key already exists."
            raise RepositoryError(msg) from e
        except PyMongoError as e:
            raise RepositoryError(f"Error updating video in MongoDB: {e}") from e

        if not updated_doc:
            raise RepositoryError(f"Video with id {video_id} not found for update.")
        return Video(**updated_doc)

    async def delete(self, video_id: str) -> Video:
        _id: ObjectId = self._validate_video_id(video_id=video_id)
        try:
            deleted_doc = await self.collection.find_one_and_delete(filter={"_id": _id})
        except PyMongoError as e:
            raise RepositoryError(f"Error deleting video from MongoDB: {e}")

        if not deleted_doc:
            raise RepositoryError(f"Video with id {video_id} not found for deletion.")
        return Video(**deleted_doc)
