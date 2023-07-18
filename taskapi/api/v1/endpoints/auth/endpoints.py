from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session
from .utils import authenticate_user, create_access_token

from .config import API_PREFIX, TOKEN_URL
from .schemas import UserData, Token

router = APIRouter(prefix=API_PREFIX)


@router.post(TOKEN_URL, response_model=Token)
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
