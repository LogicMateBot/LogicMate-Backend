from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# Conexión a MongoDB principal
def get_main_db() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017/?authSource=admin")
    return client["logicmate_main"]

# Conexión a MongoDB Studio
def get_studio_db() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27018/?authSource=admin")
    return client["logicmate_studio"]
