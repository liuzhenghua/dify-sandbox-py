import asyncio
import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from config import app_config


class ConcurrencyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.semaphore = asyncio.Semaphore(app_config.MAX_WORKERS)
        self.current_requests = 0

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/v1/sandbox/run"):
            start_time = time.perf_counter()
            request.app.state.current_requests = self.current_requests
            if self.current_requests >= app_config.MAX_REQUESTS:
                logging.warning(
                    f"Too many requests, current requests: {self.current_requests}, "
                    f"max requests: {app_config.MAX_REQUESTS}"
                )
                return JSONResponse(
                    status_code=429,
                    content={
                        "code": 429,
                        "message": f"Too Many Requests, max requests: {app_config.MAX_REQUESTS}",
                        "data": None
                    }
                )

            self.current_requests += 1
            request.app.state.current_requests = self.current_requests
            try:
                async with self.semaphore:
                    response = await call_next(request)
                return response
            finally:
                elapsed_time = time.perf_counter() - start_time
                logging.info(f"Request '/v1/sandbox/run' took {elapsed_time:.3f} seconds")
                self.current_requests -= 1
        return await call_next(request)
