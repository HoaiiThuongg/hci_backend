from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=100)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    display_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)