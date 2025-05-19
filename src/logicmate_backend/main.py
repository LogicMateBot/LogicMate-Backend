# uvicorn logicmate_backend.main:app --app-dir src --reload

from fastapi import FastAPI
from logicmate_backend.controllers.video_controller import router as video_router

app = FastAPI(
    title="LogicMate Backend",
    description="API para gestionar videos, escenas y explicaciones",
    version="1.0.0",
)


@app.get("/", tags=["root"])
async def health_check() -> dict:
    return {"status": "ok", "message": "LogicMate Backend running"}


app.include_router(router=video_router)
