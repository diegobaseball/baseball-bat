from fastapi import APIRouter
from apps.utils import include_routers
from apis.admin import admin
from apis.dashboard import dashboard
from apis.sync import sync

router = APIRouter(prefix="/v1")
include_routers(router, [admin, dashboard, sync])
