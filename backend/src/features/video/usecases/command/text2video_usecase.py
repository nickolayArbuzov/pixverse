from src.adapters.pixverse_adapter import PixverseAdapter
from src.features.video.repositories import VideoCommandRepository
from src.features.video.video_schema import CreateVideo


class Text2VideoCommand:
    def __init__(self, user: CreateVideo):
        self.user = user


class Text2VideoUseCase:
    def __init__(
        self,
        video_repository: VideoCommandRepository,
        pixverse_adapter: PixverseAdapter,
    ):
        self.video_repository = video_repository

    async def execute(self, command: Text2VideoCommand):
        video = await self.video_repository.Text2Video(command.user)
        return video
