import uuid
from sqlalchemy import String, Column
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base
from src.common.mixins.timestamp_mixin import TimestampMixin


class Video(TimestampMixin, Base):
    __tablename__ = "video"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    app_bundle_id = Column(String, nullable=False)
    apphud_user_id = Column(String, nullable=False)
    prompt = Column(String, nullable=True)
    status = Column(String, nullable=False)
    video_url = Column(String, nullable=True)
