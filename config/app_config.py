from pydantic_settings import SettingsConfigDict
from config.feature.server_config import ServerConfig
from config.feature.logging_config import LoggingConfig


class AppConfig(
    ServerConfig,
    LoggingConfig,
):
    model_config = SettingsConfigDict(
        # read from dotenv format config file
        env_file=".env",
        env_file_encoding="utf-8",
        frozen=False,
        # ignore extra attributes
        extra="ignore",
    )
