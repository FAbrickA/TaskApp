from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session

from .config import API_PREFIX
from .schemas import PingResponse
from .utils import health_check_db

router = APIRouter(prefix=API_PREFIX, tags=["Health"])


@router.get(
    "/ping_app",
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
)
async def ping_app():
    return PingResponse(
        message="Application is working!",
    )


@router.get(
    "/ping_db",
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Database is not working",
        },
    }
)
async def ping_db(session: Annotated[AsyncSession, Depends(get_session)]):
    if await health_check_db(session):
        return PingResponse(
            message="Database is working!",
        )
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Database isn't working(",
    )
