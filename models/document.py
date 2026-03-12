from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[str] = mapped_column(String, nullable=False)

    content: Mapped[dict] = mapped_column(JSONB, nullable=False)

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )