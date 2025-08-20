from fastapi import status


class BaseAPIException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Внутренняя ошибка сервера"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class NotFoundError(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Ресурс не найден"


class ValidationError(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ошибка валидации данных"


class ConflictError(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Конфликт данных"


class ForbiddenError(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Доступ запрещен"


class UnauthorizedError(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Не авторизован"
