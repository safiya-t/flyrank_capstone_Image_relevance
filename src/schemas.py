from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RootResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str


class ImageCreate(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    status: str = Field(default="pending", min_length=1, max_length=50)

    @field_validator("filename", "status")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class ImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    status: str
    created_at: datetime


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)

    @field_validator("title", "content")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_at: datetime
