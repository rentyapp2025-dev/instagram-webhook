from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # Tokens / IDs
    VERIFY_TOKEN: str = Field(..., description="Token para verificar webhook")
    IG_PAGE_TOKEN: str = Field(..., description="Page Access Token (Instagram)")
    IG_USER_ID: str = Field(..., description="instagram_business_account.id (IG user id)")
    APP_SECRET: str = Field("", description="App Secret (opcional, para firmar webhooks)")

    # Graph
    GRAPH_API_VERSION: str = Field("v18.0", description="Versión del Graph API")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
