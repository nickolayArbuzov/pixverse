import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.broker.subscriber import start_consumer
from src.features.outbox.cron import run_outbox_publisher
from src.database import Base, engine
from src.features.playwright import playwright_model
from src.features.outbox import outbox_model
from src.features.inbox import inbox_model


async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        asyncio.create_task(run_outbox_publisher())
        asyncio.create_task(start_consumer())
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
