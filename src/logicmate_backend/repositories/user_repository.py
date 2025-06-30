from typing import Any, Dict, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from collections.abc import Mapping
from pymongo.errors import PyMongoError, DuplicateKeyError
from pymongo.results import InsertOneResult
from bson.errors import InvalidId

from logicmate_backend.models.user import User
from logicmate_backend.repositories.errors import RepositoryError


class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
        self.collection = self.db["users"]

    def _validate_user_id(self, user_id: str) -> ObjectId:
        try:
            return ObjectId(oid=user_id)
        except InvalidId as e:
            raise RepositoryError(f"Invalid user ID format: {user_id}") from e

    async def get_all(self) -> List[User]:
        try:
            mongo_users_json: List[Dict] = await self.collection.find({}).to_list(
                length=100
            )
        except PyMongoError as e:
            raise RepositoryError(f"Error retrieving users from MongoDB: {e}")

        users: List[User] = [User(**user) for user in mongo_users_json]

        return users

    async def get_by_id(self, user_id: str) -> Optional[User]:
        _id: ObjectId = self._validate_user_id(user_id=user_id)

        try:
            user = await self.collection.find_one(filter={"_id": _id})
        except PyMongoError as e:
            raise RepositoryError(f"Error retrieving user by ID from MongoDB: {e}")

        if user is None:
            return None

        return User(**user)

    async def get_by_email(self, email: str) -> Optional[User]:
        try:
            user = await self.collection.find_one(filter={"email": email})
        except PyMongoError as e:
            raise RepositoryError(f"Error retrieving user by email from MongoDB: {e}")

        if user is None:
            return None

        return User(**user)

    async def create(self, user_dict: dict) -> Optional[User]:
        try:
            result: InsertOneResult = await self.collection.insert_one(
                document=user_dict
            )

        except DuplicateKeyError as e:
            details: Any | Dict[Any, Any] = getattr(e, "details", {}) or {}
            key_pattern = details.get("keyPattern", {})

            if "username" in key_pattern:
                msg = "This username is already taken."
            elif "email" in key_pattern:
                msg = "This email is already registered."
            else:
                msg = "A user with this identifier already exists."
            raise RepositoryError(msg) from e

        except PyMongoError as e:
            raise RepositoryError(f"Error creating user in MongoDB: {e}")

        created_user: User | None = await self.get_by_id(
            user_id=str(object=result.inserted_id)
        )
        if created_user is None:
            raise RepositoryError(
                "User creation failed, user not found after insertion."
            )

        return created_user

    async def update(self, user_id: str, user_dict: dict) -> Optional[User]:
        _id: ObjectId = self._validate_user_id(user_id=user_id)

        try:
            updated_doc = await self.collection.find_one_and_update(
                filter={"_id": _id},
                update={"$set": user_dict},
                return_document=ReturnDocument.AFTER,
            )

        except DuplicateKeyError as e:
            details: Mapping[str, Any] = e.details or {}
            key_pattern = details.get("keyPattern", {})
            if "username" in key_pattern:
                msg = "This username is already taken."
            elif "email" in key_pattern:
                msg = "This email is already registered."
            else:
                msg = "A user with this identifier already exists."
            raise RepositoryError(msg) from e

        except PyMongoError as e:
            raise RepositoryError(f"Error updating user in MongoDB: {e}") from e

        if not updated_doc:
            raise RepositoryError(f"User with id {user_id} not found for update.")

        updated_user: User | None = await self.get_by_id(user_id=user_id)
        if updated_user is None:
            raise RepositoryError(f"User with id {user_id} not found after update.")

        return updated_user

    async def delete(self, user_id: str) -> Optional[User]:
        _id: ObjectId = self._validate_user_id(user_id=user_id)

        try:
            deleted_doc = await self.collection.find_one_and_delete(
                filter={"_id": _id},
            )
        except PyMongoError as e:
            raise RepositoryError(f"Error deleting user from MongoDB: {e}")

        if not deleted_doc:
            raise RepositoryError(f"User with id {user_id} not found for deletion.")

        return User(**deleted_doc)
