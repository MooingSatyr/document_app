from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User | None:
        return self.db.scalars(
            select(User).where(User.username == username)
        ).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.scalars(
            select(User).where(User.id == user_id, User.is_active == True)
        ).first()

    def create(self, username: str, hashed_password: str, role) -> User:
        user = User(
            username=username,
            hashed_password=hashed_password,
            role=role,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user