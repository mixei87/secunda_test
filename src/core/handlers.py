import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.core.exceptions import BaseAPIException

logger = logging.getLogger(__name__)


async def http_exception_handler(_: Request, exc: BaseAPIException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


async def unexpected_exception_handler(_: Request, __: Exception) -> JSONResponse:
    logger.exception("Непредвиденная ошибка")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка сервера"},
    )


def register_exception_handlers(app) -> None:
    """Регистрация обработчиков исключений"""
    app.add_exception_handler(BaseAPIException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unexpected_exception_handler)
