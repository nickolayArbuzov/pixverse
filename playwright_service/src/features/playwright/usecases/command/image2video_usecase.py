import uuid
from playwright.async_api import async_playwright
from src.common.helpers.outbox_event_creater import build_outbox_event
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
            outbox_data = build_outbox_event(
                event_type="text2video.generated",
                routing_key="main.events",
                video_id=video_id,
                status="ready",
                extra_payload={"url": "url"},
            )

            await self.outbox_repository.save(outbox_data)

        except Exception as e:
            outbox_data = build_outbox_event(
                event_type="text2video.failed",
                routing_key="main.events",
                video_id=video_id,
                status="error",
                extra_payload={"error": str(e)},
            )
            await self.outbox_repository.save(outbox_data)
            print(f"Error in playwright flow: {e}")
            raise
