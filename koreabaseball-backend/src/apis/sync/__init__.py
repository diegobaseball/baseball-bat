from apps.utils import include_routers
from apis.sync.blastmotion import blastmotion
from apis.sync.hittrax import hit_trax
from fastapi import APIRouter

sync = APIRouter(
    prefix="/sync",
    tags=["Data Synchronization"],
)
include_routers(sync, [blastmotion, hit_trax])
