import asyncio
from sqlalchemy import select, update
from src.features.outbox.outbox_model import OutboxModel
from src.broker.publisher import publish_event
from src.dependencies import session_scope
from src.database import AsyncSessionLocal


async def run_outbox_publisher():
    while True:
        try:
            async with session_scope(AsyncSessionLocal) as session:
                events = (
                    (
                        await session.execute(
                            select(OutboxModel)
                            .where(OutboxModel.processed == False)
                            .limit(50)
                        )
                    )
                    .scalars()
                    .all()
                )
                for event in events:
                    try:
                        await publish_event(
                            event.event_type, event.payload, event.routing_key
                        )
                        await session.execute(
                            update(OutboxModel)
                            .where(OutboxModel.id == event.id)
                            .values(processed=True)
                        )
                    except Exception as e:
                        print(f"Event-error: {event.id}: {e}")
        except Exception as e:
            print(f"Batch-error: {e}")
        await asyncio.sleep(10)
