from fastapi import APIRouter

from app.api.routes import question_generation

api_router = APIRouter()

# TODO: Add routes as needed
api_router.include_router(question_generation.router, prefix="/question_generation", tags=["question_generation"])