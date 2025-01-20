import logging
import pytz
import functools
from datetime import datetime, timezone

from fastapi import FastAPI

from config import app_config


def _time_converter(seconds, tz):
    return datetime.fromtimestamp(seconds, tz=timezone.utc).astimezone(tz).timetuple()


def init_app(app: FastAPI):
    # add logging filter
    logging_filter = LoggingFilter(app)
    logger = logging.getLogger()
    logger.addFilter(logging_filter)

    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.addFilter(logging_filter)

    # format log timezone
    log_tz = app_config.LOG_TZ
    if log_tz:
        tz = pytz.timezone(log_tz)
        for handler in logging.root.handlers:
            handler.formatter.converter = functools.partial(_time_converter, tz=tz)

class LoggingFilter(logging.Filter):

    def __init__(self, app: FastAPI):
        self.app = app

    def filter(self, record):
        record.max_workers = app_config.MAX_WORKERS
        record.current_requests = getattr(self.app.state, 'current_requests', 0)
        return True
