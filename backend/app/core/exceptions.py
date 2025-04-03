from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional

class CustomException(HTTPException):
    """Base class for custom exceptions"""
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class DatabaseError(CustomException):
    """Exception raised for database-related errors"""
    def __init__(self, detail: str = "Database error occurred"):
        super().__init__(status_code=500, detail=detail)


class NotFoundError(CustomException):
    """Exception raised when a resource is not found"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class ForbiddenError(CustomException):
    """Exception raised when access to a resource is forbidden"""
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(status_code=403, detail=detail)


class ValidationError(CustomException):
    """Exception raised for validation errors"""
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=422, detail=detail)


# Exception handlers
async def database_exception_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    """Handler for database exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "database_error"}
    )


async def not_found_exception_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    """Handler for not found exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "not_found"}
    )


async def forbidden_exception_handler(request: Request, exc: ForbiddenError) -> JSONResponse:
    """Handler for forbidden exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "forbidden"}
    )


async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handler for validation exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "validation_error"}
    )


def add_exception_handlers(app):
    """Add exception handlers to FastAPI app"""
    app.add_exception_handler(DatabaseError, database_exception_handler)
    app.add_exception_handler(NotFoundError, not_found_exception_handler)
    app.add_exception_handler(ForbiddenError, forbidden_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)