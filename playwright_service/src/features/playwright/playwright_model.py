from sqlalchemy import Integer, String, Column

from src.database import Base
from src.common.mixins.timestamp_mixin import TimestampMixin


class Video(TimestampMixin, Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True, index=True)
    app_bundle_id = Column(String)
    apphud_user_id = Column(String)
    prompt = Column(String)
    status = Column(String)
    url = Column(String)
