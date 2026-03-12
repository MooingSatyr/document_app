from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserCreate(BaseModel):
    password: str = Field(min_length=8, description="Пароль (минимум 8 символов)")
    username: str = Field(description="Логин пользователя")
    role: str = Field(
        default="commoner",
        pattern="^(commoner|scientist)$",
        description="Роль: 'commoner', 'scientist'",
    )


class User(BaseModel):
    id: int
    username: str
    is_active: bool
    role: str
    model_config = ConfigDict(from_attributes=True)

class RefreshTokenRequest(BaseModel):
    refresh_token: str
