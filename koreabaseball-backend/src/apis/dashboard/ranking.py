from apps.db import SessionDep
from apps.admin.auth import (
    JWTBearer,
    token_required,
)
from fastapi import APIRouter, Depends

ranking = APIRouter(
    prefix="/ranking",
    tags=["dashboard"],
)


@ranking.get("/rank")
@token_required
async def rank_data(date: str, session: SessionDep, dependencies=Depends(JWTBearer())):
    return
