from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self.db.get(User, user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return (await self.db.execute(statement)).scalar_one_or_none()

    async def get_by_display_name(self, display_name: str) -> Optional[User]:
        statement = select(User).where(User.display_name == display_name)
        return (await self.db.execute(statement)).scalar_one_or_none()

    async def get_all(self) -> list[User]:
        statement = select(User).order_by(User.id)
        return list((await self.db.scalars(statement)).all())

    async def create(self, email: Optional[str], display_name: str) -> User:
        user = User(
            email=email,
            display_name=display_name,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
