import datetime as dt
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from db.session import get_session
from config import get_settings

from .config import ALGORITHM, API_PREFIX, TOKEN_URL

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/{TOKEN_URL}")


async def get_user(session: AsyncSession, email: str) -> User | None:
    return await session.query(User).filter(User.email == email).first()


async def authenticate_user(session: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user(session, email)
    if not user:
        return None
    if not user.check_password(password):
        return None
    return user


def create_access_token(payload: dict, expires_delta: dt.timedelta | None = None) -> str:
    if expires_delta is None:
        expires_delta = dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = dt.datetime.utcnow() + expires_delta

    to_encode = payload.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    # JWTError will be raised if token is invalid
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_token


async def get_current_user(
        session: Annotated[AsyncSession, Depends(get_session)],
        token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
    except JWTError:
        raise credentials_exception

    email = payload.get("email")
    if not email:
        raise credentials_exception
    user = await get_user(session, email)
    if not user:
        raise credentials_exception

    return user
