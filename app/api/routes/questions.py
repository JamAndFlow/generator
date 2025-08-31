from fastapi import APIRouter
import json

from app.schemas.utils import UserPrompt, TechDescription
from app.services.questions import add_daily_question_to_mongodb
from app.services.questions import ( 
    generate_daily_question as generate_daily_question_service,
    add_tech_description_to_store)

from app.services.questions import get_most_recent_daily_question

router = APIRouter()


@router.post("/generate_daily_question")
def generate_daily_question(request: UserPrompt):
    """
    Generate a daily question based on defined prompts
    or user's input.
    """
    response = generate_daily_question_service(user_prompt=request.user_prompt)
    try:
        question = json.loads(response)  # Parse the JSON string to a dictionary
    except json.JSONDecodeError:
        return {"error": "Failed to parse the generated question."}
    add_daily_question_to_mongodb(question)  # Store question in MongoDB
    return response


@router.post("/add_tech_description")
def add_tech_description(request: TechDescription):
    """
    Add a technical description to the vector store.
    Whenever admin add a new tech description/Tag, it will be stored in ChromaDB.
    """
    add_tech_description_to_store(description=request.description, metadata=request.metadata)
    return {"message": "Tech description added successfully."}


@router.get("/get_daily_question")
def get_daily_question():
    """
    Retrieve the most recent daily question.
    """
    recent_question = get_most_recent_daily_question()
    if recent_question:
        return recent_question
    return {"message": "No daily question found."}