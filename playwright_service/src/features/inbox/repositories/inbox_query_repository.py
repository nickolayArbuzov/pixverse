from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.features.inbox.inbox_model import InboxModel


class InboxQueryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists_by_event_id(self, event_id: str) -> bool:
        return (
            await self.session.execute(
                select(InboxModel).where(InboxModel.event_id == event_id)
            )
        ).scalar_one_or_none() is not None
