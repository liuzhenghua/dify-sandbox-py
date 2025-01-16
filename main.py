import logging
import os
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.metric import metric_router
from api.open_api import open_api_router
from config import app_config
from core import sig_term_handler, logging_filter
from core.code_executor import code_executor
from core.middleware.auth_middleware import AuthMiddleware
from core.middleware.concurrency_middleware import ConcurrencyMiddleware


@asynccontextmanager
async def lifespan(local_app: FastAPI):
    yield
    await code_executor.shutdown()

def create_app() -> FastAPI:
    local_app = FastAPI(lifespan=lifespan)

    logging.config.dictConfig(app_config.get_logging_config())
    logging_filter.init_app(local_app)
    # Initialize sig term handler to gracefully shutdown the app
    sig_term_handler.init_app(local_app)

    local_app.state.stop_event = threading.Event()
    local_app.include_router(open_api_router)
    local_app.include_router(metric_router)
    local_app.add_middleware(AuthMiddleware)
    local_app.add_middleware(ConcurrencyMiddleware)
    return local_app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    if app_config.DEBUG:
        logging.info("App running in debug mode.")
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8194,
            log_config=app_config.logging_config,
            reload=True,
        )
    else:
        worker_count = os.cpu_count()
        logging.info("App running in production mode.")
        logging.info(f"Starting Uvicorn with {worker_count} workers...")
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8194,
            log_config=app_config.logging_config,
            reload=False,
            workers=worker_count,
        )
