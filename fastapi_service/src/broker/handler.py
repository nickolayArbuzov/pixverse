import json
from aio_pika import IncomingMessage
from src.features.video.repositories import VideoCommandRepository
from src.features.video.usecases.command import (
    MarkVideoReadyUseCase,
    MarkVideoReadyCommand,
    MarkVideoErrorUseCase,
    MarkVideoErrorCommand,
)
from src.dependencies import session_scope
from src.database import AsyncSessionLocal
from src.features.inbox.repositories import (
    InboxQueryRepository,
    InboxCommandRepository,
)
from src.features.inbox.inbox_model import InboxModel

USECASE_MAP = {
    "text2video.generated": (MarkVideoReadyUseCase, MarkVideoReadyCommand),
    "text2video.failed": (MarkVideoErrorUseCase, MarkVideoErrorCommand),
}


async def on_message(msg: IncomingMessage):
    async with msg.process(requeue=True):
        try:
            body = json.loads(msg.body)
            event_type = body.get("event_type")
            payload = body.get("payload")
            event_id = payload.get("event_id") if payload else None

            if not (event_type and event_id):
                print("Malformed message, skipping.")
                return

            async with session_scope(AsyncSessionLocal) as session:
                query_repo = InboxQueryRepository(session)
                command_repo = InboxCommandRepository(session)

                exists = await query_repo.exists_by_event_id(event_id)
                if exists:
                    print(f"Skipping duplicate event: {event_id}")
                    return

                await command_repo.save(InboxModel(event_id=event_id, payload=payload))
                usecase_entry = USECASE_MAP.get(event_type)
                if usecase_entry:
                    usecase_class, command_class = usecase_entry
                    command = command_class(payload)
                    await usecase_class(
                        video_repository=VideoCommandRepository(session)
                    ).execute(command)
                else:
                    print(f"Unknown event type: {event_type}")

        except Exception as e:
            print(f"Error processing message: {e}")
            raise
