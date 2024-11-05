from fastapi import APIRouter
from apps.db import BlastMotionData, SessionDep

blastmotion = APIRouter(prefix="/blastmotion")


@blastmotion.post("/update")
async def update_data(data: BlastMotionData, session: SessionDep):
    table = BlastMotionData(**data)
    session.add(table)
    session.commit()
    session.refresh(table)
    return {"message": "Blast data received successfully"}
