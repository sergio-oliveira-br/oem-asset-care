# alert-engine/core/exceptions.py

from fastapi import Request
from fastapi.responses import JSONResponse

class AlertEngineException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

async def custom_exception_handler(request: Request, exc: AlertEngineException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.code, "message": exc.message}
    )