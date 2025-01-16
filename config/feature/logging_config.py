import logging.config
import os
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class LoggingConfig(BaseSettings):
    """
    Logging configs
    """

    LOG_LEVEL: str = Field(
        description='Log output level, default to INFO.'
        'It is recommended to set it to ERROR for production.',
        default='INFO',
    )

    LOG_FILE: Optional[str] = Field(
        description='logging output file path',
        default=None,
    )

    ACCESS_LOG_FILE: Optional[str] = Field(
        description='access logging output file path',
        default=None,
    )

    LOG_FORMAT: str = Field(
        description='log format',
        default='%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s] [] [%(filename)s#%(name)s:%(lineno)d] - %('
                'message)s',
    )

    ACCESS_LOG_FORMAT: str = Field(
        description='unicorn access log format',
        default='%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s] [] [%(filename)s#%(name)s:%(lineno)d] - %('
                'client_addr)s "%(request_line)s" %(status_code)s',
    )

    LOG_DATEFORMAT: Optional[str] = Field(
        description='log date format, eg:Asia/Shanghai',
        default='%Y-%m-%d %H:%M:%S',
    )

    LOG_TZ: Optional[str] = Field(
        description='specify log timezone, eg: America/New_York',
        default='Asia/Shanghai',
    )

    logging_config: Optional[dict] = Field(
        description='specify log config, need be a dict',
        default=None,
    )

    def __init__(self):
        super().__init__()
        self.logging_config = self.get_logging_config()
        logging.config.dictConfig(self.get_logging_config())

    def get_logging_config(self):
        if self.logging_config:
            return self.logging_config
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': self.LOG_FORMAT,
                    'datefmt': self.LOG_DATEFORMAT,
                },
                "access": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "fmt": self.ACCESS_LOG_FORMAT,
                    'datefmt': self.LOG_DATEFORMAT,
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'default'
                },
                "access": {
                    "formatter": "access",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
            },
            'root': {
                'level': self.LOG_LEVEL,
                'handlers': ['console'],
            }
        }

        log_file = self.LOG_FILE
        if log_file:
            access_log_dir = os.path.dirname(log_file)
            if access_log_dir:
                os.makedirs(access_log_dir, exist_ok=True)
            logging_config['handlers']['file'] = {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_file,
                'maxBytes': 1024 * 1024 * 1024,
                'backupCount': 5,
                'formatter': 'default',
                'encoding': 'utf8',
            }
            logging_config['root']['handlers'] = ['console', 'file']

        access_log_file = self.ACCESS_LOG_FILE
        if access_log_file:
            access_log_dir = os.path.dirname(access_log_file)
            if access_log_dir:
                os.makedirs(access_log_dir, exist_ok=True)
            logging_config['handlers']['file_access'] = {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': access_log_file,
                'maxBytes': 1024 * 1024 * 1024,
                'backupCount': 5,
                'formatter': 'access',
                'encoding': 'utf8',
            }
            logging_config['loggers']['uvicorn.access']['handlers'] = ['access', 'file_access']

        return logging_config
