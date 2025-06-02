from src.features.video.repositories import VideoCommandRepository


class MarkVideoErrorCommand:
    def __init__(self, payload: dict):
        self.video_id = payload["video_id"]
        self.status = payload["status"]
        self.error = payload.get("error")


class MarkVideoErrorUseCase:
    def __init__(self, video_repository: VideoCommandRepository):
        self.video_repository = video_repository

    async def execute(self, command: MarkVideoErrorCommand):
        await self.video_repository.update_status_and_url(
            video_id=command.video_id,
            status=command.status,
            url=None,
        )
