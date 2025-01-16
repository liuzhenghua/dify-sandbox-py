from fastapi import APIRouter

from api.entities.code_entities import Response, CodeRunResult, CodeRequest
from core.code_executor import code_executor

open_api_router = APIRouter(prefix='/v1')

@open_api_router.post("/sandbox/run")
async def execute_code(request: CodeRequest):
    if request.language not in ["python3", "nodejs"]:
        return {
            "code": -400,
            "message": "unsupported language",
            "data": None
        }
    result = await code_executor.execute(request.code, request.language)
    return Response.success(CodeRunResult(error=result["error"] or "", stdout=result["output"] or ""))
