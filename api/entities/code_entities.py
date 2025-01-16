from typing import Optional, Any

from pydantic import BaseModel


class CodeRequest(BaseModel):
    language: str
    code: str
    preload: Optional[str] = ""
    enable_network: Optional[bool] = False


class Response(BaseModel):
    code: int = 0
    message: str = "success"
    data: Optional[Any] = None

    @staticmethod
    def success(data: Optional[Any] = None):
        return Response(data=data)


class CodeRunResult(BaseModel):
    error: str = ""
    stdout: str = ""

