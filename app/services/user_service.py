from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from typing import Optional

class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def create_user(self, data: UserCreate) -> User:
        email = str(data.email).strip().lower()

        existing_user = self.user_repository.get_by_email(email)

        if existing_user is not None:
            raise ValueError("Email already exists")

        return self.user_repository.create(
            email=email,
            display_name=data.display_name.strip(),
        )

    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repository.get_by_id(user_id)

    def get_users(self) -> list[User]:
        return self.user_repository.get_all()