from apps.db import SessionDep
from apps.admin.auth import (
    JWTBearer,
    token_required,
)
from fastapi import APIRouter, Depends

summary = APIRouter(
    prefix="/summary",
    tags=["dashboard"],
)


@summary.get("/average")
@token_required
async def average_data(
    date: str, session: SessionDep, dependencies=Depends(JWTBearer())
):
    return
