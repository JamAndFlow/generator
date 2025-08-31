from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.settings import settings

app = FastAPI(
    title="Generator Service",
    description="API for generating and managing coding problems",
    version="0.1.0"
)

app.include_router(api_router, prefix=settings.API_V1_STR, tags=["v1"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "JamAndFlow-generator"}