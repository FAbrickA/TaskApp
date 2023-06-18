from fastapi import FastAPI, APIRouter


def bind_routes(
        application: FastAPI | APIRouter,
        list_of_routers: list[APIRouter],
        prefix="",
):
    for router in list_of_routers:
        application.include_router(router, prefix=prefix)
