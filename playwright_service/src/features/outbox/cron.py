import asyncio
from src.broker.publisher import publish_event
from src.dependencies import session_scope
from src.database import AsyncSessionLocal
from src.features.outbox.repositories import OutboxQueryRepository


async def run_outbox_publisher():
    while True:
        try:
            async with session_scope(AsyncSessionLocal) as session:
                query_repo = OutboxQueryRepository(session)

                events = await query_repo.get_many(50)

                for event in events:
                    try:
                        await publish_event(
                            event.event_type,
                            event.payload,
                            event.routing_key,
                        )

                        event.processed = True
                        await session.flush()

                    except Exception as e:
                        print(f"Event-error: {event.id}: {e}")

        except Exception as e:
            print(f"Batch-error: {e}")

        await asyncio.sleep(10)
