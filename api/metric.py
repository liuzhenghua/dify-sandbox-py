import os

from fastapi import APIRouter
from starlette.requests import Request

from config import app_config

metric_router = APIRouter()


@metric_router.get('/metrics')
async def get_metrics(request: Request):
    app = request.app
    data = {}
    pid = os.getpid()
    data['pid'] = pid
    data['max_workers'] = app_config.MAX_WORKERS
    data['max_requests'] = app_config.MAX_REQUESTS
    data['current_requests'] = app.state.current_requests if hasattr(app.state, 'current_requests') else 0
    return data

@metric_router.get("/health")
async def health_check(request: Request):
    if request.app.state.stop_event.is_set():
        return "stopped", 500
    return "ok"
