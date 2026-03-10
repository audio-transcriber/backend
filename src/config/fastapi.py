from pydantic_settings import BaseSettings, SettingsConfigDict


class FastAPISettings(BaseSettings):
    allow_origins: list[str]

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='fastapi_',
        extra='ignore',
    )


fastapi_settings = FastAPISettings()
