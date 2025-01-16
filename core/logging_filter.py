import logging

from fastapi import FastAPI

from config import app_config


def init_app(app: FastAPI):
    logging_filter = LoggingFilter(app)
    logger = logging.getLogger()
    logger.addFilter(logging_filter)

    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.addFilter(logging_filter)

class LoggingFilter(logging.Filter):

    def __init__(self, app: FastAPI):
        self.app = app

    def filter(self, record):
        record.max_workers = app_config.MAX_WORKERS
        record.current_requests = getattr(self.app.state, 'current_requests', 0)
        return True
