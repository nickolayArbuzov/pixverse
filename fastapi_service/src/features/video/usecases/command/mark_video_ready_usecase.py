from src.features.video.repositories import VideoCommandRepository


class MarkVideoReadyCommand:
    def __init__(self, payload: dict):
        self.video_id = payload["video_id"]
        self.url = payload["url"]
        self.status = payload["status"]


class MarkVideoReadyUseCase:
    def __init__(self, video_repository: VideoCommandRepository):
        self.video_repository = video_repository

    async def execute(self, command: MarkVideoReadyCommand):
        await self.video_repository.update_status_and_url(
            video_id=command.video_id,
            status=command.status,
            url=command.url,
        )
