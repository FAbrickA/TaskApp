from typing import Annotated

from fastapi import APIRouter, Response, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from db.session import get_session

router = APIRouter()


@router.get("/ping")
async def ping():
    return Response(
        "pong",
        status_code=status.HTTP_200_OK,
    )


@router.get("/test_db")
async def test_db(session: Annotated[AsyncSession, Depends(get_session)]):
    stmt = select(User).limit(1)
    result = await session.execute(stmt)
    user = result.one_or_none()
    print(user)
    return Response(
        str(user),
        status_code=status.HTTP_200_OK,
    )
