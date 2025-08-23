from fastapi import APIRouter
from app.services.questions import generate_daily_question as generate_daily_question_service, add_daily_question_to_store as add_question_in_chroma_db, add_daily_question_to_mongodb
from app.schemas.utils import UserPrompt
router = APIRouter()


@router.post("/generate_daily_question")
def generate_daily_question(request: UserPrompt):
    """
    Generate a daily question based on defined prompts
    or user's input.
    """
    response = generate_daily_question_service(user_prompt=request.user_prompt)
    add_daily_question_to_mongodb(response)  # Store question in MongoDB
    return response

@router.get("/get_daily_question")
def get_daily_question():
    """
    Retrieve the most recent daily question.
    """
    #TODO: implement this endpoint
    # Get from mongoDB
    return {"message": "This endpoint will return the most recent daily question. Not implemented yet."}