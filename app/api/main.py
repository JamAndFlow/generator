from fastapi import APIRouter

from app.api.routes import questions

api_router = APIRouter()

# TODO: Add routes as needed
api_router.include_router(questions.router, prefix="/questions", tags=["question_generation"])