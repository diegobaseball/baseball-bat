from config import DMOTION_APP_ID
from config import DMOTION_API_KEY
from datetime import timedelta
from httpx import AsyncClient


class DMotionClient:
    def __init__(self):
        self.client = AsyncClient(base_url="https://api.4dmotionsports.com")

    async def retrieve_access_token(self) -> str:
        params = {"app_id": DMOTION_APP_ID}
        payload = {"secret": DMOTION_API_KEY}
        response = await self.client.post(
            "/public/v1.1/access-token", params=params, json=payload
        )
        response.raise_for_status()
        return response.json()["access_token"]

    async def export(self, _from: timedelta, until: timedelta, mode: int):
        token = await self.retrieve_access_token()
        headers = {"X-Auth-Token": token}
        match mode:
            case 0:
                _mode = "all"
            case 1:
                _mode = "graph"
            case 2:
                _mode = "raw"
            case 3:
                _mode = "metrics"
            case _:
                raise ValueError("Invalid mode")
        params = {
            "zoneId": "Europe/Budapest",
            "from": _from,
            "until": until,
            "mode": _mode,
            "subject": "all",
        }
        response = await self.client.get(
            "/public/v1.1/sensor-measurements.export", headers=headers, params=params
        )
        response.raise_for_status()
        return response.json()
