from fastapi import FastAPI
from .ig import router as ig_router


def create_app() -> FastAPI:
    app = FastAPI(title="Instagram Webhook (FastAPI)")

    # Salud
    @app.get("/")
    async def health():
        return {"status": "ok", "service": "instagram-webhook"}

    # Rutas de Instagram
    app.include_router(ig_router, prefix="/instagram")

    return app


# 👇 Import target para Uvicorn en Render
app = create_app()
