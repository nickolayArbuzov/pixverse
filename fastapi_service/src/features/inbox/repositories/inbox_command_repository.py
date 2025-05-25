from sqlalchemy.ext.asyncio import AsyncSession
from src.features.inbox.inbox_model import InboxModel


class InboxCommandRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, inbox_model: InboxModel) -> None:
        self.session.add(inbox_model)
        await self.session.flush()
