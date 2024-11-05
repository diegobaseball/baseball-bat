from apps.db import SessionDep
from apps.admin.auth import (
    JWTBearer,
    token_required,
)
from fastapi import APIRouter, Depends

training = APIRouter(
    prefix="/training",
    tags=["dashboard"],
)


@training.get("/get")
@token_required
async def training_data(
    month: str,
    day: str,
    year: str,
    session: SessionDep,
    dependencies=Depends(JWTBearer()),
):
    return


@training.get("/input")
@token_required
async def training_data_input(
    month: str,
    day: str,
    year: str,
    data: dict,
    session: SessionDep,
    dependencies=Depends(JWTBearer()),
):
    return
