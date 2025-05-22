from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update, insert

from src.features.video.video_schema import CreateVideo
from src.features.video.video_model import Video


class VideoCommandRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def Text2Video(self, video: CreateVideo) -> None:
        result = (
            await self.session.execute(
                insert(Video).values(**video.model_dump()).returning(Video)
            )
        ).scalar()
        return result

    async def Image2Video(self, video: CreateVideo) -> None:
        result = (
            await self.session.execute(
                insert(Video).values(**video.model_dump()).returning(Video)
            )
        ).scalar()
        return result
