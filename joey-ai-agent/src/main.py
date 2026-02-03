import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.config import settings
from src.api.health import router as health_router
from src.api.line_webhook import router as line_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info(f"Starting Joey's AI Agent in {settings.app_env} mode")
    logger.info(f"Server: {settings.host}:{settings.port}")
    yield
    logger.info("Shutting down Joey's AI Agent")


app = FastAPI(
    title="Joey's AI Agent",
    description="LINE → Claude → Notion AI Assistant",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(health_router)
app.include_router(line_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.app_env == "development"
    )
