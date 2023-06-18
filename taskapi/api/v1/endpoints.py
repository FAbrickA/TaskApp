from fastapi import APIRouter, Response, status

router = APIRouter()


@router.get("/ping")
async def ping():
    return Response(
        "pong",
        status_code=status.HTTP_200_OK,
    )

