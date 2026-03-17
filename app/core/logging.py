import logging
from logging.config import dictConfig

from app.core.request_context import get_request_id


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "request_id_filter": {
                    "()": "app.core.logging.RequestIdFilter",
                }
            },
            "formatters": {
                "standard": {
                    "format": (
                        "%(asctime)s %(levelname)s "
                        "[%(name)s] [request_id=%(request_id)s] %(message)s"
                    )
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "filters": ["request_id_filter"],
                    "formatter": "standard",
                    "level": "INFO",
                }
            },
            "root": {
                "handlers": ["console"],
                "level": "INFO",
            },
        }
    )