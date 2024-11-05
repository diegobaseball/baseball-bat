from apps.utils import include_routers
from apis.admin.account import account
from fastapi import APIRouter


admin = APIRouter(
    prefix="/admin",
)
include_routers(admin, [account])
