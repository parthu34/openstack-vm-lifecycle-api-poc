import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.models.common import ErrorDetail, ErrorResponse

logger = logging.getLogger("app.errors")


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(
        request: Request,
        exc: AppException,
    ) -> JSONResponse:
        logger.warning(
            "app_exception path=%s code=%s status_code=%s",
            request.url.path,
            exc.code,
            exc.status_code,
        )

        response = ErrorResponse(
            error=ErrorDetail(
                code=exc.code,
                message=exc.message,
                details=exc.details,
            )
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        logger.warning(
            "validation_exception path=%s error_count=%s",
            request.url.path,
            len(exc.errors()),
        )

        response = ErrorResponse(
            error=ErrorDetail(
                code="request_validation_error",
                message="Request validation failed",
                details={"errors": exc.errors()},
            )
        )
        return JSONResponse(
            status_code=422,
            content=response.model_dump(),
        )