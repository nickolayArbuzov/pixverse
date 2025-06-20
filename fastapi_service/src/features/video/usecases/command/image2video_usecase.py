import uuid
from fastapi import UploadFile
from src.common.helpers.outbox_event_creater import build_outbox_event
from src.features.video.repositories import VideoCommandRepository, FileAdapter
from src.features.video.video_schema import InputVideoImageRequest, VideoInDB
from src.features.outbox.repositories import OutboxCommandRepository


class Image2VideoCommand:
    def __init__(self, video_request: InputVideoImageRequest, file: UploadFile):
        self.video_request = video_request
        self.file = file


class Image2VideoUseCase:
    def __init__(
        self,
        video_repository: VideoCommandRepository,
        outbox_repository: OutboxCommandRepository,
        file_adapter: FileAdapter,
    ):
        self.video_repository = video_repository
        self.outbox_repository = outbox_repository
        self.file_adapter = file_adapter

    async def execute(self, command: Image2VideoCommand):
        video_id = str(uuid.uuid4())
        image_filename = f"{video_id}.png"
        image_path = f"/shared/{image_filename}"

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
            extra_payload={
                "image_path": image_path,
            },
        )

        await self.outbox_repository.save(outbox_data)

        await self.file_adapter.write_file(filename=image_filename, file=command.file)

        return video
