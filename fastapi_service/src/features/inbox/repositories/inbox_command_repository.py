from sqlalchemy.ext.asyncio import AsyncSession
from src.features.inbox.inbox_model import InboxModel


class InboxCommandRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, inbox_data: InboxModel) -> None:
        inbox_model = InboxModel(**inbox_data)
        self.session.add(inbox_model)
        await self.session.flush()
