from pydantic import BaseModel, Field
from datetime import datetime


class CreateVideo(BaseModel):
    app_bundle_id: str = Field(...)
    apphud_user_id: str = Field(...)
    prompt: str = Field(...)
    status: str = Field(...)
    url: str = Field(...)


class ResponseVideo(CreateVideo):
    id: int
    created_at: datetime
    updated_at: datetime


class Video(BaseModel):
    id: int
    app_bundle_id: str
    apphud_user_id: str
    prompt: str
    status: str
    url: str

    class Config:
        orm_mode = True
