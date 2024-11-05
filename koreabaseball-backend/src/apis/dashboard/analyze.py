from apps.db import SessionDep
from apps.admin.auth import (
    JWTBearer,
    token_required,
)
from fastapi import APIRouter, Depends

analyze = APIRouter(
    prefix="/analyze",
    tags=["dashboard"],
)


@analyze.get("/day")
@token_required
async def analyze_data(
    date: str, session: SessionDep, dependencies=Depends(JWTBearer())
):
    return
