# uvicorn logicmate_backend.main:app --app-dir src --reload

from contextlib import asynccontextmanager
from fastapi import FastAPI
from logicmate_backend.config.db import get_main_db
from logicmate_backend.controllers.user_controller import router as user_router
from logicmate_backend.controllers.auth_controller import router as auth_router
from logicmate_backend.controllers.video_controller import router as video_router
from pymongo.errors import PyMongoError
from dotenv import load_dotenv


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_main_db()
    try:
        await db.command(command="ping")
    except PyMongoError as e:
        raise RuntimeError(f"Failed to connect to MongoDB: {e}")
    yield


load_dotenv()
app = FastAPI(
    title="LogicMate Backend",
    description="LogicMate Backend API, a RESTful API for LogicMate",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get(path="/health", tags=["root"])
async def health_check() -> dict:
    return {"status": "ok", "message": "LogicMate Backend running"}


app.include_router(
    router=user_router,
)
app.include_router(
    router=auth_router,
)
app.include_router(
    router=video_router,
)
