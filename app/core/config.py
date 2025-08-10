from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    app_name: str = Field(default="Day Guard AI", alias="APP_NAME")
    env: str = Field(default="development", alias="ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    port: int = Field(default=8000, alias="PORT")

    # Database
    database_url: str = Field(default="sqlite:///./dayguard.db", alias="DATABASE_URL")

    # AI providers
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    mistral_api_key: str | None = Field(default=None, alias="MISTRAL_API_KEY")
    gemini_api_key: str | None = Field(default=None, alias="GEMINI_API_KEY")

    # Telegram
    telegram_bot_token: str | None = Field(default=None, alias="TELEGRAM_BOT_TOKEN")

    # Integrations
    google_calendar_credentials_path: str | None = Field(
        default=None, alias="GOOGLE_CALENDAR_CREDENTIALS_PATH"
    )
    google_maps_api_key: str | None = Field(default=None, alias="GOOGLE_MAPS_API_KEY")
    ifttt_webhook_key: str | None = Field(default=None, alias="IFTTT_WEBHOOK_KEY")
    zapier_hook_url: str | None = Field(default=None, alias="ZAPIER_HOOK_URL")

    # MCP
    mcp_server_url: str | None = Field(default=None, alias="MCP_SERVER_URL")


settings = Settings()
