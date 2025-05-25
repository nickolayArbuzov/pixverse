from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.outbox.outbox_model import OutboxModel


class OutboxQueryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_many(self, count: int) -> List[OutboxModel]:
        return (
            (
                await self.session.execute(
                    (
                        select(OutboxModel)
                        .where(OutboxModel.processed == False)
                        .order_by(OutboxModel.created_at.asc())
                        .limit(count)
                    )
                )
            )
            .scalars()
            .all()
        )
