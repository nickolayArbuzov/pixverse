from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.features.video.video_model import Video


class VideoQueryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def GetStatusGenerate(self, video_id: int) -> Video:
        video_query = text(
            """
                SELECT
                    "video".id AS video_id,
                    "video".status AS video_status,
                    "video".url AS video_url
                FROM "video"
                WHERE "video".id = :video_id
            """
        )
        rows = await self.session.execute(video_query, {"video_id": video_id})
        column_headers = list(rows.keys())
        data = rows.fetchall()

        def map_query_result_to_json(data, column_headers):
            result = {"video": None}
            for row in data:
                video_id = row[column_headers.index("video_id")]
                if result["video"] is None:
                    result["video"] = {
                        "id": video_id,
                        "status": row[column_headers.index("video_status")],
                        "url": row[column_headers.index("video_url")],
                    }
                    video_obj = result["video"]
            return result

        _, value = next(iter(map_query_result_to_json(data, column_headers).items()))
        return value
