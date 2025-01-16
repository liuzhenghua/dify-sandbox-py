import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from config import app_config


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/v1/sandbox"):
            api_key = request.headers.get("X-Api-Key")
            if not api_key or api_key != app_config.API_KEY:
                from fastapi.responses import JSONResponse

                logging.warning("Unauthorized access to sandbox API")
                return JSONResponse(
                    status_code=401,
                    content={
                        "code": 401,
                        "message": "Unauthorized",
                        "data": None
                    }
                )
        return await call_next(request)
