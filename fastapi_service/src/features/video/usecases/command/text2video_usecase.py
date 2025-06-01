import uuid
from src.common.helpers.outbox_event_creater import build_outbox_event
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
        future_video_path_in_container = f"/shared/{video_id}.mp4"

        video_to_create = VideoInDB(
            id=video_id,
            app_bundle_id=command.video_request.app_bundle_id,
            apphud_user_id=command.video_request.apphud_user_id,
            prompt=command.video_request.prompt,
            status="requested",
            video_url=None,
        )
        video = await self.video_repository.request_video(video_to_create)

        outbox_data = build_outbox_event(
            event_type="image2video.requested",
            routing_key="playwright.events",
            video_id=video.id,
            prompt=video.prompt,
            future_video_path_in_container=future_video_path_in_container,
        )

        await self.outbox_repository.save(outbox_data)

        return video
