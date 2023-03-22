from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv(verbose=True)


class CommonSettings(BaseSettings):
    APP_NAME: str = Field(..., env="APP_NAME")
    DEBUG_MODE: bool = Field(True, env="DEBUG_MODE")


class ServerSettings(BaseSettings):
    HOST: str = Field("localhost", env="HOST")
    PORT: int = Field(8000, env="PORT")


class DatabaseSettings(BaseSettings):
    NEO4J_URI: str = Field(..., env="NEO4J_URI")
    NEO4J_USERNAME: str = Field(..., env="NEO4J_USERNAME")
    NEO4J_PASSWORD: str = Field(..., env="NEO4J_PASSWORD")


class CacheSettings(BaseSettings):
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")
    REDIS_PASSWORD: str = Field(..., env="REDIS_PASSWORD")


class Settings(CommonSettings, ServerSettings, DatabaseSettings,
               CacheSettings):
    pass
