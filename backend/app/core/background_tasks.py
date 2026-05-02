from __future__ import annotations

import asyncio

from app.core.websocket_manager import WebSocketManager
from app.services.admin_analytics import AdminLiveAnalyticsService
from app.services.pest_alert_service import PestAlertService
from app.services.realtime_prediction import RealTimePredictionService
from app.services.weather_stream import WeatherStreamService


class BackgroundTaskOrchestrator:
    def __init__(self) -> None:
        self.manager = WebSocketManager()
        self.admin_service = AdminLiveAnalyticsService(self.manager)
        self.pest_service = PestAlertService(self.manager, self.admin_service)
        self.prediction_service = RealTimePredictionService(self.admin_service)
        self.weather_service = WeatherStreamService(self.manager, self.pest_service, self.admin_service)
        self._tasks: list[asyncio.Task] = []
        self._started = False

    async def startup(self) -> None:
        if self._started:
            return
        self._started = True
        self._tasks = [
            asyncio.create_task(self.weather_service.run_forever()),
            asyncio.create_task(self.admin_service.run_forever()),
        ]

    async def shutdown(self) -> None:
        self._started = False
        await self.weather_service.stop()
        await self.admin_service.stop()
        for task in self._tasks:
            task.cancel()
        for task in self._tasks:
            try:
                await task
            except Exception:
                pass
        self._tasks.clear()


orchestrator = BackgroundTaskOrchestrator()
