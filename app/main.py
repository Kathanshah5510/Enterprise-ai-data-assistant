from fastapi import FastAPI

from app.api.health import router as health_router

app = FastAPI(
    title="Enterprise AI Data Assistant",
    version="1.0.0",
)

app.include_router(health_router)


@app.get("/")
def home() -> dict[str, str]:
    """Get API status."""
    return {
        "message": "Enterprise AI Data Assistant API is running!"
    }