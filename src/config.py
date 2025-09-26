from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    LOG_LEVEL: str = "DEBUG"


settings = Settings()
