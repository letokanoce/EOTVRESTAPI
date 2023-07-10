from typing import TypeVar

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv(verbose=True)


class Settings(BaseSettings):
    pass


SettingsT = TypeVar(name='SettingsT', bound=Settings)


class CommonSettings(Settings):
    APP_NAME: str = Field(..., env='APP_NAME')
    DEBUG_MODE: bool = Field(True, env='DEBUG_MODE')
    HOST: str = Field(..., env='HOST')
    PORT: int = Field(..., env='PORT')


class Neo4jSettings(Settings):
    NEO4J_URI: str = Field(..., env='NEO4J_URI')
    NEO4J_USERNAME: str = Field(..., env='NEO4J_USERNAME')
    NEO4J_PASSWORD: str = Field(..., env='NEO4J_PASSWORD')


class RedisSettings(Settings):
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")
    REDIS_PASSWORD: str = Field(..., env="REDIS_PASSWORD")
