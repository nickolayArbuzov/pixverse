from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class InputVideo(BaseModel):
    app_bundle_id: str = Field(..., example="com.myapp.bundle")
    apphud_user_id: str = Field(..., example="user_123")
    prompt: str = Field(..., example="A futuristic city at night")
    image_to_generate: Optional[str] = Field(
        None, example="https://example.com/image.png"
    )


class VideoInDB(BaseModel):
    app_bundle_id: str
    apphud_user_id: str
    prompt: str
    image_to_generate: Optional[str] = None
    status: str
    url: Optional[str] = None

    class Config:
        orm_mode = True


class ResponseVideo(VideoInDB):
    id: int
    created_at: datetime
    updated_at: datetime
