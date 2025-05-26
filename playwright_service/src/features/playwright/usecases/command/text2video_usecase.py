import uuid
from playwright.async_api import async_playwright
from src.settings import pixverse_credentials
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

        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()

                await page.goto(
                    "https://app.pixverse.ai/onboard", wait_until="domcontentloaded"
                )
                print("Page loaded:", await page.title())

                login_button = page.locator("button:has(span:text-is('Login'))").first
                await login_button.evaluate("el => el.innerText")
                await login_button.click(force=True)
                print("Clicked Login")

                await page.wait_for_selector("#Username")
                await page.fill("#Username", pixverse_credentials.PIXVERSE_USERNAME)
                print("Entered username")

                await page.wait_for_selector("#Password")
                await page.fill("#Password", pixverse_credentials.PIXVERSE_PASSWORD)
                print("Entered password")

                login_button = page.locator("button:has(span:text-is('Login'))").first
                await login_button.evaluate("el => el.innerText")
                await login_button.click(force=True)
                print("Clicked Login")

                textareas = page.locator(
                    'textarea[placeholder="Describe the content you want to create"]'
                )
                count = await textareas.count()

                for i in range(count):
                    el = textareas.nth(i)
                    if await el.is_visible():
                        print(f"✅ Using visible textarea #{i}")
                        await el.fill(prompt)
                        break
                print("Prompt filled")

                create_button = page.locator("button:has(span:text-is('Create'))").first
                await create_button.evaluate("el => el.innerText")
                await create_button.click(force=True)
                print("Create button clicked")

                #await page.wait_for_selector("text=Video ready", timeout=60000)
                #print("Video is ready!")
                await browser.close()

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
