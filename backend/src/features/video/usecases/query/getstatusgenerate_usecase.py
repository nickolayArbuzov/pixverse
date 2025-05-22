from src.adapters.pixverse_adapter import PixverseAdapter
from src.features.video.repositories import VideoQueryRepository


class GetStatusGenerateQuery:
    def __init__(self, user: CreateUser):
        self.user = user


class GetStatusGenerateUseCase:
    def __init__(
        self, video_repository: VideoQueryRepository, pixverse_adapter: PixverseAdapter
    ):
        self.video_repository = video_repository

    async def execute(self, query: GetStatusGenerateQuery):
        video = await self.video_repository.GetStatusGenerate(query.user)
        return video
