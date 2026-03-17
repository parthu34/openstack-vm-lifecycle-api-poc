import logging
import time
from uuid import uuid4

from fastapi import Request
from starlette.responses import Response

from app.core.request_context import reset_request_id, set_request_id

logger = logging.getLogger("app.request")


async def request_context_middleware(request: Request, call_next) -> Response:
    request_id = request.headers.get("X-Request-ID", uuid4().hex)
    token = set_request_id(request_id)
    request.state.request_id = request_id
    start_time = time.perf_counter()

    logger.info(
        "request_started method=%s path=%s",
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)
    except Exception:
        process_time_ms = (time.perf_counter() - start_time) * 1000
        logger.exception(
            "request_failed method=%s path=%s process_time_ms=%.2f",
            request.method,
            request.url.path,
            process_time_ms,
        )
        reset_request_id(token)
        raise

    process_time_ms = (time.perf_counter() - start_time) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-Ms"] = f"{process_time_ms:.2f}"

    logger.info(
        "request_completed method=%s path=%s status_code=%s process_time_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        process_time_ms,
    )

    reset_request_id(token)
    return response