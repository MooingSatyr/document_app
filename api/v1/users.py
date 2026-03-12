from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from core.dependencies import get_db
from repositories.user import UserRepository
from services.user_service import UserService
from schemas.users import UserCreate, User, RefreshTokenRequest


router = APIRouter(prefix="/users", tags=["users"])


def get_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, service: UserService = Depends(get_service)):
    return service.create_user(user.username, user.password, user.role)


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_service),
):
    return service.login(form_data.username, form_data.password)


@router.post("/refresh")
def refresh_token(
    body: RefreshTokenRequest,
    service: UserService = Depends(get_service),
):
    return service.refresh(body.refresh_token)