from apps.db import SessionDep
from apps.admin.auth import (
    JWTBearer,
    token_required,
)
from fastapi import APIRouter, Depends

report = APIRouter(
    prefix="/report",
    tags=["dashboard"],
)


@report.get("/download")
@token_required
async def report_download(
    date: str, data_type: str, session: SessionDep, dependencies=Depends(JWTBearer())
):
    return
