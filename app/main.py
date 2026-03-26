from fastapi import FastAPI

from app.config.config import settings

print("[DEBUG] app.main loaded")
print(f"[DEBUG] settings: app_name={settings.app_name}, app_debug={settings.app_debug}")


def create_app() -> FastAPI:
    print("[DEBUG] create_app() called")
    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
        docs_url="/docs" if settings.app_debug else None,
        redoc_url="/redoc" if settings.app_debug else None,
    )

    @app.get("/health", status_code=200, tags=["Health"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    print("[DEBUG] Running as script (py -m app.main)")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=settings.app_debug)

