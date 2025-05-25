import uuid
from playwright.async_api import async_playwright
from src.features.outbox.repositories import OutboxCommandRepository


class Text2VideoCommand:
    def __init__(self, payload: dict):
        self.payload = payload


class Text2VideoUseCase:
    def __init__(self, outbox_repository: OutboxCommandRepository):
        self.outbox_repository = outbox_repository

    async def execute(self, command: Text2VideoCommand):
        video_id = command.payload["video_id"]
        prompt = command.payload["prompt"]
        app_bundle_id = command.payload.get("app_bundle_id")
        apphud_user_id = command.payload.get("apphud_user_id")

        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto("https://app.pixverse.ai/home")
                content = await page.content()
                print(content[:500])
                await browser.close()

            outbox_event = {
                "event_type": "text2video.generated",
                "routing_key": "main.events",
                "payload": {
                    "video_id": video_id,
                    "url": url,
                    "status": "ready",
                    "app_bundle_id": app_bundle_id,
                    "apphud_user_id": apphud_user_id,
                    "event_id": str(uuid.uuid4()),
                },
                "processed": False,
            }
            await self.outbox_repository.Save(outbox_event)

        except Exception as e:
            outbox_event = {
                "event_type": "text2video.failed",
                "routing_key": "main.events",
                "payload": {
                    "video_id": video_id,
                    "status": "error",
                    "app_bundle_id": app_bundle_id,
                    "apphud_user_id": apphud_user_id,
                    "event_id": str(uuid.uuid4()),
                    "error": str(e),
                },
                "processed": False,
            }
            await self.outbox_repository.save(outbox_event)
            print(f"Error in playwright flow: {e}")
            raise
