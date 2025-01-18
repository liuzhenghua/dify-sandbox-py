import multiprocessing

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from config import app_config

metric_router = APIRouter()


@metric_router.get('/metrics')
async def get_metrics(request: Request):
    app = request.app
    data = {}
    data['process_name'] = multiprocessing.current_process().name
    data['max_workers'] = app_config.MAX_WORKERS
    data['max_requests'] = app_config.MAX_REQUESTS
    data['current_requests'] = app.state.current_requests if hasattr(app.state, 'current_requests') else 0
    return data

@metric_router.get("/health")
async def health_check(request: Request):
    if request.app.state.stop_event.is_set():
        return PlainTextResponse("stopped", status_code=503)
    return "ok"
