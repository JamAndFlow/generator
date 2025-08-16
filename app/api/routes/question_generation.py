from fastapi import APIRouter, Depends
from app.services.generate_daily_question import  generate_daily_question, add_question_in_chroma_db 

router = APIRouter()


@router.post("/")
def generate_daily_question_1():
    """
    Generate a daily question based on the user's input.
    """

    response =  generate_daily_question()
    add_question_in_chroma_db(response.content)
    return response