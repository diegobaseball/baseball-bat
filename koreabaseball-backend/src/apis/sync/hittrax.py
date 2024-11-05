from fastapi import APIRouter
from fastapi import APIRouter
from apps.db import HitTraxData, SessionDep


hit_trax = APIRouter(prefix="/hit_trax")


@hit_trax.post("/update")
async def update_data(data: HitTraxData, session: SessionDep):
    table = HitTraxData(**data)
    session.add(table)
    session.commit()
    session.refresh(table)

    return {"message": "HitTrax data received successfully"}
