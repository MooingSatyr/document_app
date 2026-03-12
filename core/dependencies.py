from sqlalchemy.orm import Session
from sqlalchemy import select
from collections.abc import Generator
import jwt

from fastapi import Depends, HTTPException, status

from core.database import SessionLocal
from core.config import settings
from core.auth import oauth2_scheme

from models.user import User as UserModel


def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.scalars(
        select(UserModel).where(
            UserModel.id == int(user_id),
            UserModel.is_active == True
        )
    ).first()

    if user is None:
        raise credentials_exception

    return user