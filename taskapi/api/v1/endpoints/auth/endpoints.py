from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from db.session import get_session
from .utils import authenticate_user, create_access_token, get_user

from .config import API_PREFIX, TOKEN_URL
from .schemas import UserData, Token, RegistrationData

router = APIRouter(prefix=API_PREFIX, tags=["Auth"])


@router.post(
    TOKEN_URL,
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Incorrect password",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Cannot find the user",
        },
    }
)
async def login_for_access_token(
        user_data: UserData,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    user = await authenticate_user(session, user_data.email, user_data.password)
    access_token = create_access_token({"email": user.email})
    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.post(
    "/signup",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "User already exists",
        },
    }
)
async def signup(
        reg_data: RegistrationData,
        session: Annotated[AsyncSession, Depends(get_session)]
):
    user = await get_user(session, reg_data.email)

    # if user with such login already exists, throw exception
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    user = User(
        email=reg_data.email,
    )
    user.set_password(reg_data.password)
    session.add(user)
    await session.commit()
