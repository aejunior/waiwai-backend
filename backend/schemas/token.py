from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    subject: str | None = None


class Subject(BaseModel):
    name: str
    email: EmailStr
