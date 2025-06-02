from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, insert

from src.features.video.video_schema import VideoInDB
from src.features.video.video_model import Video


class VideoCommandRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def request_video(self, video: VideoInDB) -> Video:
        result = (
            await self.session.execute(
                insert(Video).values(**video.model_dump()).returning(Video)
            )
        ).scalar()
        return result

    async def update_status_and_url(self, video_id: str, status: str, url: str | None):
        await self.session.execute(
            (
                update(Video)
                .where(Video.id == video_id)
                .values(status=status, video_url=url)
                .execution_options(synchronize_session="fetch")
            )
        )
