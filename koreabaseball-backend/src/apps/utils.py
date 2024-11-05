from fastapi import APIRouter


def include_routers(app: APIRouter, router_list: list[APIRouter]):
    for router in router_list:
        app.include_router(router)


__all__ = ["include_routers"]
