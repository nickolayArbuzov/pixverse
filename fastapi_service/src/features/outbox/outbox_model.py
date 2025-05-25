from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import JSONB
from src.common.mixins.timestamp_mixin import TimestampMixin
from src.database import Base


class OutboxModel(TimestampMixin, Base):
    __tablename__ = "outbox"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)
    routing_key = Column(String, nullable=False)
    payload = Column(JSONB, nullable=False)
    processed = Column(Boolean, default=False)
