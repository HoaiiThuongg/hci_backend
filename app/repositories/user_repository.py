from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from typing import Optional

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def get_all(self) -> list[User]:
        statement = select(User).order_by(User.id)
        return list(self.db.scalars(statement).all())

    def create(self, email: str, display_name: str) -> Optional[User]:
        user = User(
            email=email,
            display_name=display_name,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user