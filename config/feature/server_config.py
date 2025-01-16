from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class ServerConfig(BaseSettings):
    DEBUG: Optional[bool] = Field(description="debug mode", default=False)
    API_KEY: str = Field(description="API key for the server", default="dify-sandbox")
    MAX_REQUESTS: int = Field(description="Maximum active request", default=60)
    MAX_WORKERS: int = Field(description="Maximum number of workers", default=50)
    WORKER_TIMEOUT: int = Field(description="Timeout for the worker in seconds", default=15)
