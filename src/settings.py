from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Tokens / secrets
    VERIFY_TOKEN: str = Field(..., env="VERIFY_TOKEN", description="Token para verificar el webhook")
    IG_APP_SECRET: str = Field(..., env="IG_APP_SECRET", description="App Secret de Instagram/Facebook")

    # Instagram Graph
    IG_PAGE_ID: str = Field(..., env="IG_PAGE_ID", description="ID de la página de Facebook conectada")
    IG_PAGE_TOKEN: str = Field(..., env="IG_PAGE_TOKEN", description="Page access token con permisos de IG")
    IG_BUSINESS_ID: str = Field(..., env="IG_BUSINESS_ID", description="Instagram Business Account ID")

    # Config
    APP_BASE_URL: str | None = Field(
        default=None,
        env="APP_BASE_URL",
        description="URL pública del webhook (ej: https://instagram-webhook-xxxxx.onrender.com)",
    )
    GRAPH_API_VERSION: str = Field(
        default="v18.0",
        env="GRAPH_API_VERSION",
        description="Versión de Graph API (ej: v18.0, v21.0)",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
