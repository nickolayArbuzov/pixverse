from src.features.video.repositories import VideoQueryRepository


class GetStatusGenerateQuery:
    def __init__(self, video_id: int):
        self.video_id = video_id


class GetStatusGenerateUseCase:
    def __init__(self, video_repository: VideoQueryRepository):
        self.video_repository = video_repository

    async def execute(self, query: GetStatusGenerateQuery):
        video = await self.video_repository.GetStatusGenerate(query.video_id)
        return video
