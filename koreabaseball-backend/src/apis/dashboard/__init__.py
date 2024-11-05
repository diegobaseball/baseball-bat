from apps.utils import include_routers
from apis.dashboard.summary import summary
from apis.dashboard.analyze import analyze
from apis.dashboard.ranking import ranking
from apis.dashboard.report import report
from apis.dashboard.training import training


from fastapi import APIRouter

dashboard = APIRouter(prefix="/dashboard")
include_routers(dashboard, [summary, analyze, ranking, report, training])
