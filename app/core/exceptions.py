"""Chuẩn hoá error response theo contract: {error_code, message, details}."""
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Map message → error_code để FE hiển thị thông báo tiếng Việt đúng ngữ cảnh
_CODE_HINTS = [
    ("display name already exists", "USER_ALREADY_EXISTS"),
    ("email already exists", "USER_ALREADY_EXISTS"),
    ("user not found", "USER_NOT_FOUND"),
    ("lesson item not found", "LESSON_ITEM_NOT_FOUND"),
    ("lesson not found", "LESSON_NOT_FOUND"),
    ("attempt not found", "ATTEMPT_NOT_FOUND"),
    ("no progress found", "ATTEMPT_NOT_FOUND"),
    ("collector", "COLLECTOR_NOT_FOUND"),
]


def guess_error_code(message: str, status_code: int) -> str:
    lower = message.lower()
    for hint, code in _CODE_HINTS:
        if hint in lower:
            return code
    if status_code == 409:
        return "USER_ALREADY_EXISTS"
    if status_code == 404:
        return "NOT_FOUND"
    if status_code == 422:
        return "VALIDATION_ERROR"
    if status_code >= 500:
        return "INTERNAL_ERROR"
    return "VALIDATION_ERROR"


def error_response(status_code: int, message: str, details=None, error_code: str | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error_code": error_code or guess_error_code(message, status_code),
            "message": message,
            "details": details,
        },
    )


async def http_exception_handler(request: Request, exc):
    detail = exc.detail if isinstance(exc.detail, str) else "Yêu cầu không hợp lệ."
    return error_response(exc.status_code, detail)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first = exc.errors()[0] if exc.errors() else {}
    field = ".".join(str(p) for p in first.get("loc", []) if p not in ("body",))
    return error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        f"Dữ liệu gửi đi chưa hợp lệ{f' ({field})' if field else ''}.",
        details=[{"loc": list(e.get("loc", [])), "msg": e.get("msg")} for e in exc.errors()],
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Lỗi phía server — thử lại sau ít phút.")
