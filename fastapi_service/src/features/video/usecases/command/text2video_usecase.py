import uuid
from src.features.video.repositories import VideoCommandRepository
from src.features.video.video_schema import InputVideoTextRequest, VideoInDB
from src.features.outbox.repositories import OutboxCommandRepository


class Text2VideoCommand:
    def __init__(self, video_request: InputVideoTextRequest):
        self.video_request = video_request


class Text2VideoUseCase:
    def __init__(
        self,
        video_repository: VideoCommandRepository,
        outbox_repository: OutboxCommandRepository,
    ):
        self.video_repository = video_repository
        self.outbox_repository = outbox_repository

    async def execute(self, command: Text2VideoCommand):
        video_id = str(uuid.uuid4())
        future_video_path = f"/shared/{video_id}.mp4"
        video_to_create = VideoInDB(
            id=video_id,
            app_bundle_id=command.video_request.app_bundle_id,
            apphud_user_id=command.video_request.apphud_user_id,
            prompt=command.video_request.prompt,
            status="requested",
            video_url=future_video_path,
        )
        video = await self.video_repository.text_2_video(video_to_create)

        outbox_data = {
            "event_type": "text2video.requested",
            "routing_key": "playwright.events",
            "payload": {
                "video_id": str(video.id),
                "prompt": video.prompt,
                "video_output_path": future_video_path,
                "event_id": str(uuid.uuid4()),
            },
            "processed": False,
        }

        await self.outbox_repository.save(outbox_data)

        return video
