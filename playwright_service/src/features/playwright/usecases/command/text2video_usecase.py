import asyncio
from playwright.async_api import async_playwright
from src.common.helpers.catch_video_id import catch_video_id
from src.settings import pixverse_credentials
from src.common.helpers.outbox_event_creater import build_outbox_event
from src.features.outbox.repositories import OutboxCommandRepository
from src.features.playwright.repositories import FileAdapter
import asyncio

_playwright_lock = asyncio.Semaphore(1)


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
        async with _playwright_lock:
            video_id = command.payload["video_id"]
            prompt = command.payload["prompt"]
            video_id_future = asyncio.get_running_loop().create_future()
            try:
                async with async_playwright() as pw:
                    browser = await pw.chromium.launch(headless=True)
                    context = await browser.new_context(accept_downloads=True)
                    page = await context.new_page()
                    page.on(
                        "response",
                        lambda res: asyncio.create_task(
                            catch_video_id(res, video_id_future)
                        ),
                    )
                    print("🌐 Переход на сайт...")
                    await page.goto(
                        "https://app.pixverse.ai/onboard", wait_until="domcontentloaded"
                    )
                    print("🔐 Авторизация...")
                    await page.click(
                        "button:has(span:text-is('Login')), button:has(span:text-is('Вход'))"
                    )
                    await page.fill("#Username", pixverse_credentials.PIXVERSE_USERNAME)
                    await page.fill("#Password", pixverse_credentials.PIXVERSE_PASSWORD)
                    await page.click(
                        "button:has(span:text-is('Login')), button:has(span:text-is('Вход'))"
                    )
                    print("🔓 Login...")
                    print("⏳ Ожидание поля ввода (textarea)...")
                    await page.wait_for_selector(
                        'textarea[placeholder="Describe the content you want to create"], textarea[placeholder="Опишите контент, который хотите создать"]',
                        timeout=60000,
                    )
                    print("✅ Поле ввода найдено...")
                    textarea = page.locator(
                        'textarea[placeholder="Describe the content you want to create"], textarea[placeholder="Опишите контент, который хотите создать"]'
                    ).first
                    await textarea.fill(prompt)
                    print("Заполняем...")
                    buttons = page.locator(
                        "button:has(span:text-is('Create')), button:has(span:text-is('Создать'))"
                    )
                    count = await buttons.count()
                    for i in range(count):
                        btn = buttons.nth(i)
                        if await btn.is_visible():
                            print(f"👉 Кликаем по видимой кнопке #{i}")
                            await btn.click()
                            break
                    else:
                        raise Exception("❌ Не найдена видимая кнопка Create/Создать")
                    print("Видео создаётся")
                    video_id_resolved = await asyncio.wait_for(
                        video_id_future, timeout=30
                    )
                    video_url = f"https://app.pixverse.ai/create?detail=show&id={video_id_resolved}&platform=web"
                    print(f"➡️ Переход к видео: {video_url}")
                    await page.goto(video_url, wait_until="domcontentloaded")

                    print("⏬ Ожидание кнопки Download...")
                    await page.wait_for_selector(
                        "button:has-text('Download'), button:has(span:text-is('Скачать'))",
                        timeout=60000,
                    )

                    print("📥 Кликаем по кнопке Download...")
                    async with page.expect_download(timeout=60000) as download_info:
                        await page.click(
                            "button:has-text('Download'), button:has(span:text-is('Скачать'))"
                        )
                    print("📥 Скачивание...")
                    download = await download_info.value

                    await self.file_adapter.save_download(
                        f"{video_id_resolved}.mp4", download
                    )

                    await browser.close()

                outbox_data = build_outbox_event(
                    event_type="text2video.generated",
                    routing_key="main.events",
                    video_id=video_id,
                    status="ready",
                    extra_payload={"url": video_url},
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
                return
