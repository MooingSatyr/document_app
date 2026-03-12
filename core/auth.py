from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import jwt

from core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire,
        "token_type": "access"
    })

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode.update({
        "exp": expire,
        "token_type": "refresh"
    })

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)