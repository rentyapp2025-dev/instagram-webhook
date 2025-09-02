from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Tokens / secrets
    VERIFY_TOKEN: str = Field(..., description="Token para verificar el webhook")
    IG_APP_SECRET: str = Field(..., description="App Secret de Instagram/Facebook")

    # Instagram Graph
    IG_PAGE_ID: str = Field(..., description="ID de la página de Facebook conectada")
    IG_PAGE_TOKEN: str = Field(..., description="Page access token con permisos de IG")
    IG_BUSINESS_ID: str = Field(..., description="Instagram Business Account ID")

    # URL pública del servicio (Render)
    APP_BASE_URL: str = Field(
        default="",
        description="URL pública del webhook (ej: https://instagram-webhook-xxxxx.onrender.com)",
    )

    # Configuración de carga desde .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignora variables no usadas
    )


settings = Settings()
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Tokens / secrets
    VERIFY_TOKEN: str = Field(..., description="Token para verificar el webhook")
    IG_APP_SECRET: str = Field(..., description="App Secret de Instagram/Facebook")

    # Instagram Graph
    IG_PAGE_ID: str = Field(..., description="ID de la página de Facebook conectada")
    IG_PAGE_TOKEN: str = Field(..., description="Page access token con permisos de IG")
    IG_BUSINESS_ID: str = Field(..., description="Instagram Business Account ID")

    # URL pública del servicio (Render)
    APP_BASE_URL: str = Field(
        default="",
        description="URL pública del webhook (ej: https://instagram-webhook-xxxxx.onrender.com)",
    )

    # Configuración de carga desde .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignora variables no usadas
    )


settings = Settings()
