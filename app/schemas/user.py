from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    # Email tuỳ chọn — S0 (design Signora) cho phép bỏ trống; FE tự sinh placeholder nếu cần
    email: str | None = Field(default=None, max_length=255)
    display_name: str = Field(min_length=1, max_length=100)


class UserRead(BaseModel):
    id: int
    email: str | None = Field(default=None, max_length=255)
    display_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
