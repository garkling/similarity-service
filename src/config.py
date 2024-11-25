from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogConfig(BaseModel):

    LOG_FORMAT: str = "%(levelprefix)s %(asctime)s - %(message)s"
    LOG_LEVEL: str = "INFO"

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        "root": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
    }


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openapi_key: str
    pinecone_key: str
    pinecone_idx: str
    initial_whitepaper_url: str = "https://services.google.com/fh/files/misc/ai_adoption_framework_whitepaper.pdf"


@lru_cache
def get_config():
    return Config()


@lru_cache
def get_logger_config():
    return LogConfig()
