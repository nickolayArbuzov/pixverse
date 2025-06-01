import uuid
from playwright.async_api import async_playwright
from src.settings import pixverse_credentials
from src.features.outbox.repositories import OutboxCommandRepository


class Image2VideoCommand:
    def __init__(self, payload: dict):
        self.payload = payload


class Image2VideoUseCase:
    def __init__(self, outbox_repository: OutboxCommandRepository):
        self.outbox_repository = outbox_repository

    async def execute(self, command: Image2VideoCommand):
        video_id = command.payload["video_id"]
        prompt = command.payload["prompt"]
        print("------------------------------------------", video_id)
        try:
            outbox_event = {
                "event_type": "text2video.generated",
                "routing_key": "main.events",
                "payload": {
                    "video_id": video_id,
                    "url": "url",
                    "status": "ready",
                    "event_id": str(uuid.uuid4()),
                },
                "processed": False,
            }
            await self.outbox_repository.save(outbox_event)

        except Exception as e:
            outbox_event = {
                "event_type": "text2video.failed",
                "routing_key": "main.events",
                "payload": {
                    "video_id": video_id,
                    "status": "error",
                    "event_id": str(uuid.uuid4()),
                    "error": str(e),
                },
                "processed": False,
            }
            await self.outbox_repository.save(outbox_event)
            print(f"Error in playwright flow: {e}")
            raise
