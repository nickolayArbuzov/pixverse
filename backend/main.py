from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import Base, engine
from src.features.video import video_controller
from src.features.video import video_model

async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(video_controller.router, prefix='/api', tags=['video'])


