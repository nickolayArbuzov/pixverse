from typing import Optional
from fastapi import Form
from pydantic import BaseModel, Field
from datetime import datetime


class InputVideoTextRequest(BaseModel):
    app_bundle_id: str = Field(..., example="com.myapp.bundle")
    apphud_user_id: str = Field(..., example="user_123")
    prompt: str = Field(..., example="A futuristic city at night")


class InputVideoImageRequest(BaseModel):
    app_bundle_id: str = Field(..., example="com.myapp.bundle")
    apphud_user_id: str = Field(..., example="user_123")
    prompt: Optional[str] = Field(None, example="A futuristic city at night")

    @classmethod
    def as_form(
        cls,
        app_bundle_id: str = Form(...),
        apphud_user_id: str = Form(...),
        prompt: Optional[str] = Form(None),
    ) -> "InputVideoImageRequest":
        return cls(
            app_bundle_id=app_bundle_id,
            apphud_user_id=apphud_user_id,
            prompt=prompt,
        )


class VideoInDB(BaseModel):
    id: str
    app_bundle_id: str
    apphud_user_id: str
    prompt: Optional[str] = None
    status: str
    video_url: Optional[str] = None

    class Config:
        orm_mode = True


class ResponseVideo(VideoInDB):
    created_at: datetime
    updated_at: datetime
