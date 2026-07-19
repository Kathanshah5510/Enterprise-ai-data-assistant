from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.v1.budgets import router as budgets_router
from app.api.v1.departments import router as departments_router
from app.api.v1.employees import router as employees_router
from app.api.v1.projects import router as projects_router

app = FastAPI(
    title="Enterprise AI Data Assistant",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(departments_router, prefix="/api/v1")
app.include_router(employees_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(budgets_router, prefix="/api/v1")


@app.get("/")
def home() -> dict[str, str]:
    """Get API status."""
    return {"message": "Enterprise AI Data Assistant API is running!"}
