from pydantic import BaseModel, EmailStr, Field, field_validator
from .base import Base, PermissionType


class UserPublic(BaseModel):
    id: int
    first_name: str = Field(min_length=3, max_length=15)
    last_name: str = Field(min_length=3, max_length=15)
    full_name: str = Field(min_length=7, max_length=31)
    email: EmailStr


class UserCreate(BaseModel):
    first_name: str = Field(min_length=3, max_length=15)
    last_name: str = Field(min_length=3, max_length=15)
    email: EmailStr
    password: str = Field(min_items=8, max_length=32)

    @field_validator('password', mode='before')
    def password_must_be_strong(cls, v: str):
        assert any(char.isdigit() for char in v), "Deve conter pelo menos um dígito."
        assert any(char.isupper() for char in v), "Deve conter pelo menos uma letra minúscula."
        assert any(char.islower() for char in v), "Deve conter pelo menos uma letra maiúscula."

        return v

    @field_validator('first_name', 'last_name')
    def first_name_alphanumeric(cls, v: str):
        assert v.isalnum(), 'Deve ser alfanumérico'
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_items=8, max_length=32)


class User(Base, UserCreate):
    pass


class UserAuth(Base):
    email: EmailStr
    permission: PermissionType


class UserUpdate(UserCreate):
    pass
