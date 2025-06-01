import aiohttp
from playwright.async_api import async_playwright
from src.settings import pixverse_credentials
from src.common.helpers.outbox_event_creater import build_outbox_event
from src.features.outbox.repositories import OutboxCommandRepository
from src.features.playwright.repositories import FileAdapter


class Text2VideoCommand:
    def __init__(self, payload: dict):
        self.payload = payload


class Text2VideoUseCase:
    def __init__(
        self, outbox_repository: OutboxCommandRepository, file_adapter: FileAdapter
    ):
        self.outbox_repository = outbox_repository
        self.file_adapter = file_adapter

    async def execute(self, command: Text2VideoCommand):
        video_id = command.payload["video_id"]
        prompt = command.payload["prompt"]
        video_path = command.payload["future_video_path_in_container"]
        video_filename = video_path.split("/")[-1]

        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()

                await page.goto(
                    "https://app.pixverse.ai/onboard", wait_until="domcontentloaded"
                )

                await page.click("button:has(span:text-is('Login'))")
                await page.fill("#Username", pixverse_credentials.PIXVERSE_USERNAME)
                await page.fill("#Password", pixverse_credentials.PIXVERSE_PASSWORD)
                await page.click("button:has(span:text-is('Login'))")
                await page.wait_for_selector("text=Create")

                textarea = page.locator(
                    'textarea[placeholder="Describe the content you want to create"]'
                )
                await textarea.fill(prompt)

                await page.click("button:has(span:text-is('Create'))")

                await page.wait_for_selector("video source", timeout=120_000)
                video_url = await page.locator("video source").get_attribute("src")
                print(f"Video URL: {video_url}")

                await browser.close()

            async with aiohttp.ClientSession() as session:
                async with session.get(video_url) as resp:

                    class StreamFile:
                        async def read(self, size: int = 1024 * 1024):
                            return await resp.content.read(size)

                    await self.file_adapter.write_file(video_filename, StreamFile())

            outbox_data = build_outbox_event(
                event_type="text2video.generated",
                routing_key="main.events",
                video_id=video_id,
                status="ready",
                extra_payload={"url": video_path},
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
            print(f"Error in text2video flow: {e}")
            raise
