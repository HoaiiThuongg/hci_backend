from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def create_user(self, data: UserCreate) -> User:
        # Spec F1: hồ sơ phân biệt người bằng display_name (unique) — trùng tên → 409
        existing = await self.user_repository.get_by_display_name(data.display_name.strip())
        if existing is not None:
            raise ValueError("Display name already exists")

        email = str(data.email).strip().lower() if data.email else None
        if email:
            existing_email = await self.user_repository.get_by_email(email)
            if existing_email is not None:
                raise ValueError("Email already exists")

        return await self.user_repository.create(
            email=email,
            display_name=data.display_name.strip(),
        )

    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.user_repository.get_by_id(user_id)

    async def get_users(self) -> list[User]:
        return await self.user_repository.get_all()
