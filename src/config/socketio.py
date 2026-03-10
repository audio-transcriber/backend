from pydantic_settings import BaseSettings, SettingsConfigDict


class SocketIOSettings(BaseSettings):
    cors_allowed_origins: list[str]

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='socketio_',
        extra='ignore',
    )


socketio_settings = SocketIOSettings()
