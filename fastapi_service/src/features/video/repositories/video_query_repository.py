from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.features.video.video_model import Video


class VideoQueryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_status_generate(self, video_id: int) -> dict:
        result = (
            await self.session.execute(
                (select(Video.id, Video.status, Video.url).where(Video.id == video_id))
            )
        ).first()

        if not result:
            return None

        return {
            "id": result.id,
            "status": result.status,
            "url": result.url,
        }
