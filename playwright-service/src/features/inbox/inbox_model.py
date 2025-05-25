from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import JSONB
from src.database import Base


class InboxModel(Base):
    __tablename__ = "inbox"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, nullable=False)
    payload = Column(JSONB, nullable=False)

