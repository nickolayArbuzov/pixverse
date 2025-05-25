from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update, insert

from src.features.video.video_schema import VideoInDB
from src.features.video.video_model import Video


class VideoCommandRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def text_2_video(self, video: VideoInDB) -> Video:
        result = (
            await self.session.execute(
                insert(Video).values(**video.model_dump()).returning(Video)
            )
        ).scalar()
        return result

    async def image_2_video(self, video: VideoInDB) -> Video:
        result = (
            await self.session.execute(
                insert(Video).values(**video.model_dump()).returning(Video)
            )
        ).scalar()
        return result
