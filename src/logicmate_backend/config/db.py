import os
from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


@lru_cache()
def _get_db_client() -> AsyncIOMotorClient:
    MONGO_DB_URL: str | None = os.environ.get("MONGO_LOCAL_URL")
    return AsyncIOMotorClient(host=MONGO_DB_URL)


def get_main_db() -> AsyncIOMotorDatabase:
    MONGO_DB_NAME: str = os.environ.get("MONGO_INITDB_DATABASE", default="logicmate_db")
    return _get_db_client()[MONGO_DB_NAME]
