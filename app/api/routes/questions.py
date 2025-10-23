import json
from typing import List

from fastapi import APIRouter, Depends, Request

from app.schemas.utils import QuestionFilters, TechDescription, UserPrompt
from app.services.questions import (add_daily_question_to_mongodb,
                                    add_tech_description_to_store)
from app.services.questions import \
    generate_daily_question as generate_daily_question_service
from app.services.questions import (get_most_recent_daily_question,
                                    get_question_by_id, list_questions)

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
    add_tech_description_to_store(
        description=request.description, metadata=request.metadata
    )
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


@router.get("/list_questions")
async def list_questions_endpoint(
    request: Request,
    page: int = 1,
    per_page: int = 10,
    title: str | None = None,
    tags: str | None = None,
    difficulty: str | None = None,
    status: str | None = None,
    description: str | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    """
    Retrieve all questions with filtering and pagination support.
    
    Parameters:
        page: Current page number (starts from 1)
        per_page: Number of items per page (10-100)
        title: Filter by title (case-insensitive partial match)
        tags: Comma-separated list of tags to filter by
        difficulty: Filter by difficulty level
        status: Filter by status
        description: Filter by description (case-insensitive partial match)
        sort_by: Field to sort by (default: created_at)
        sort_order: Sort order (asc/desc)
    """
    # Convert comma-separated tags string to list if provided
    tag_list = tags.split(",") if tags else None
    
    result = list_questions(
        page=page,
        per_page=per_page,
        title=title,
        tags=tag_list,
        difficulty=difficulty,
        status=status,
        description=description,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    # Generate next page URL if available
    total_pages = result["total_pages"]
    current_page = page
    
    if current_page < total_pages:
        base_url = str(request.base_url)
        query_params = dict(request.query_params)
        query_params["page"] = str(current_page + 1)
        result["next_page"] = f"{base_url}list_questions?{'&'.join(f'{k}={v}' for k, v in query_params.items())}"
    else:
        result["next_page"] = None
        
    return result


@router.get("/get_question/{question_id}")
def get_question(question_id: str):
    """
    Retrieve a specific question by ID.
    
    Parameters:
        question_id: The unique identifier of the question
    """
    question = get_question_by_id(question_id)
    if question:
        return question
    return {"message": "Question not found"}