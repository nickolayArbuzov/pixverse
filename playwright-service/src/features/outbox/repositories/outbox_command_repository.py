from sqlalchemy.ext.asyncio import AsyncSession

from src.features.outbox.outbox_model import OutboxModel


class OutboxCommandRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def Save(self, outbox_model: OutboxModel) -> None:
        self.session.add(outbox_model)
        await self.session.flush()
