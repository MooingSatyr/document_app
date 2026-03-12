from fastapi import HTTPException, status
from core.auth import hash_password, verify_password, create_access_token, create_refresh_token
from core.config import settings
from repositories.user import UserRepository
import jwt


class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, username: str, password: str, role):
        if self.repo.get_by_username(username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        hashed = hash_password(password)
        return self.repo.create(username, hashed, role)

    def login(self, username: str, password: str):
        user = self.repo.get_by_username(username)

        if not user or not user.is_active or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        return {
            "access_token": create_access_token({"sub": str(user.id), "role": user.role}),
            "refresh_token": create_refresh_token({"sub": str(user.id), "role": user.role}),
            "token_type": "bearer",
        }

    def refresh(self, refresh_token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token",
        )

        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            token_type = payload.get("token_type")

            if user_id is None or token_type != "refresh":
                raise credentials_exception

        except jwt.PyJWTError:
            raise credentials_exception

        user = self.repo.get_by_id(int(user_id))

        if user is None:
            raise credentials_exception

        return {
            "access_token": create_access_token({"sub": str(user.id), "role": user.role}),
            "token_type": "bearer",
        }