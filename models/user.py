from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLAEnum

from core.database import Base
from enum import Enum

class UserRole(str, Enum):
    SCIENTIST = "scientist"
    COMMONER = "commoner"


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[UserRole] = mapped_column(SQLAEnum(UserRole), default=UserRole.COMMONER)
