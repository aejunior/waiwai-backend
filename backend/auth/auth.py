import time

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from jose.jwt import JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import auth_handler
from backend.configs import Settings, get_async_session
from backend.models import User
from backend.schemas import Subject, Token, TokenData, UserAuth
from backend.utils import create_access_token, create_refresh_token

settings = Settings()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def sign_jwt(subject: Subject) -> Token:
    access_token = create_access_token(subject, settings)
    refresh_token = create_refresh_token(subject, settings)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='Bearer',
    )


def decode_jwt_exp(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(
            token,
            settings.jwt_secret_key_access_token,
            algorithms=[settings.jwt_algorithm],
        )
        return decoded_token if decoded_token['exp'] >= time.time() else None
    except JWTError:
        return None


def decode_jwt_sub(token: str) -> dict | None:
    payload = jwt.decode(
        token,
        settings.jwt_secret_key_access_token,
        algorithms=[settings.jwt_algorithm],
    )
    return payload['sub']


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
    session: AsyncSession = Depends(get_async_session),
    credentials: HTTPAuthorizationCredentials = Depends(auth_handler.security),
) -> UserAuth:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível validar credenciais.',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        sub = decode_jwt_sub(credentials.credentials)
        if not sub:
            raise credentials_exception
        token_data = TokenData(subject=sub)
    except JWTError:
        raise credentials_exception

    statement = select(User).where(User.email == token_data.subject)

    result = await session.execute(statement)
    user: User | None = result.scalar_one_or_none()
    # logger.debug(user.permission)
    if user is None:
        raise credentials_exception

    return UserAuth(id=user.id, email=user.email, permission=user.permission)
