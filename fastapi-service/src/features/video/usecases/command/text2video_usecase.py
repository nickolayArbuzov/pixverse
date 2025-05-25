import uuid
from src.features.video.repositories import VideoCommandRepository
from src.features.video.video_schema import CreateVideo
from src.features.outbox.repositories import OutboxCommandRepository


class Text2VideoCommand:
    def __init__(self, video: CreateVideo):
        self.video = video


class Text2VideoUseCase:
    def __init__(
        self,
        video_repository: VideoCommandRepository,
        outbox_repository: OutboxCommandRepository,
    ):
        self.video_repository = video_repository
        self.outbox_repository = outbox_repository

    async def execute(self, command: Text2VideoCommand):
        video_to_create = CreateVideo(
            app_bundle_id=command.video.app_bundle_id,
            apphud_user_id=command.video.apphud_user_id,
            prompt=command.video.prompt,
            image_to_generate=None,
            status="requested",
            url=None,
        )
        video = await self.video_repository.Text2Video(video_to_create)

        outbox_data = {
            "event_type": "text2video.requested",
            "routing_key": "playwright.events",
            "payload": {
                "video_id": video.id,
                "prompt": video.prompt,
                "event_id": str(uuid.uuid4()),
            },
            "processed": False,
        }

        await self.outbox_repository.save(outbox_data)

        return video
