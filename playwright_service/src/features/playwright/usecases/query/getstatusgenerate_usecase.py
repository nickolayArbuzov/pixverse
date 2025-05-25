class GetStatusGenerateQuery:
    def __init__(self, video_id: int):
        self.video_id = video_id


class GetStatusGenerateUseCase:

    async def execute(self, query: GetStatusGenerateQuery):
        pass
