from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.main import api_router
from app.logging_config import setup_logging
from app.scheduler import shutdown_scheduler, start_scheduler
from app.settings import settings

logger = setup_logging("Generator-Service")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Start up and shut down events for the FastAPI app."""
    logger.info("Starting FastAPI app...")
    start_scheduler()
    try:
        yield
    finally:
        shutdown_scheduler()


app = FastAPI(
    title="Generator Service",
    description="API for generating and managing coding problems",
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions globally."""
    logger.exception("Unhandled error %s in request %s", exc, request.url)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


app.include_router(api_router, prefix=settings.API_V1_STR, tags=["v1"])


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "JamAndFlow-generator"}
