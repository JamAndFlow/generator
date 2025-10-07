import uuid
from datetime import datetime

from langchain_core.documents import Document

from app.config.config_mongo_fb import questions_collection
from app.config.vectorestore import chroma_db
from app.llm.provider import invoke_with_retries
from app.pipelines.daily_question_pipeline import daily_question_chain
from app.schemas.utils import TechDescriptionMetadata


def generate_daily_question(user_prompt: str = None) -> any:
    """Generate a daily question using the LLM pipeline."""
    payload = {"user_prompt": user_prompt}
    response = invoke_with_retries(daily_question_chain, payload)
    # ChatHuggingFace returns an AIMessage by default; str() yields content.
    return response.content


# TODO: Add error handling
def add_daily_question_to_mongodb(question: dict) -> None:
    """Add a daily question to the MongoDB collection."""
    question_document = {
        "_id": f"q_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "title": question.get("title", ""),  # Extract title from question
        "description": question.get(
            "description", ""
        ),  # Extract description from question
        "created_at": datetime.utcnow().isoformat(),
        "likes": 0,
        "dislikes": 0,
        "hints": question.get("hints", []),
        "tags": question.get("tags", []),
        "difficulty": question.get("difficulty", "None"),
        "status": "published",
        "skills": question.get("learning_objectives", []),
        "categories": question.get("categories", []),
    }
    questions_collection.insert_one(question_document)


def add_tech_description_to_store(
    description: str, metadata: TechDescriptionMetadata
) -> None:
    """Add a tech description to the ChromaDB collection."""
    doc_id = str(uuid.uuid4())
    doc = Document(id=doc_id, page_content=description, metadata=metadata.model_dump())
    chroma_db.add_documents(collection="tech_description", documents=[doc])


def get_most_recent_daily_question():
    """Fetch the most recent daily question from MongoDB."""
    recent_question = questions_collection.find_one(sort=[("created_at", -1)])
    if recent_question:
        return {
            "id": recent_question["_id"],
            "title": recent_question["title"],
            "description": recent_question["description"],
            "created_at": recent_question["created_at"],
            "likes": recent_question["likes"],
            "dislikes": recent_question["dislikes"],
            "tags": recent_question["tags"],
            "difficulty": recent_question["difficulty"],
            "status": recent_question["status"],
            "hints": recent_question.get("hints", []),
            "skills": recent_question.get("learning_objectives", []),
            "categories": recent_question.get("categories", []),
        }
    return None


def list_questions(
    page: int = 1,
    per_page: int = 10,
    title: str = None,
    tags: list = None,
    difficulty: str = None,
    status: str = None,
    description: str = None,
    skills: list = None,
    categories: list = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> dict:
    """
    List questions with filtering and pagination support.
    """
    # Build the filter query
    query = {}
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    if tags:
        query["tags"] = {"$in": tags}
    if difficulty:
        query["difficulty"] = difficulty
    if status:
        query["status"] = status
    if skills:
        query["learning_objectives"] = {"$in": skills}
    if categories:
        query["categories"] = {"$in": categories}
    if description:
        query["description"] = {"$regex": description, "$options": "i"}

    # Calculate skip and limit for pagination
    skip = (page - 1) * per_page
    
    # Set sort order
    sort_direction = -1 if sort_order.lower() == "desc" else 1
    sort_criteria = [(sort_by, sort_direction)]

    # Get total count for pagination
    total_questions = questions_collection.count_documents(query)
    
    # Fetch questions with pagination
    questions = questions_collection.find(
        query,
        skip=skip,
        limit=per_page,
        sort=sort_criteria
    )

    # Convert cursor to list and format response
    questions_list = []
    for q in questions:
        questions_list.append({
            "id": q["_id"],
            "title": q["title"],
            "description": q["description"],
            "created_at": q["created_at"],
            "likes": q["likes"],
            "dislikes": q["dislikes"],
            "tags": q["tags"],
            "difficulty": q["difficulty"],
            "status": q["status"],
            "hints": q.get("hints", []),
            "skills": q.get("learning_objectives", []),
            "categories": q.get("categories", [])
        })

    return {
        "questions": questions_list,
        "total": total_questions,
        "page": page,
        "per_page": per_page,
        "total_pages": (total_questions + per_page - 1) // per_page
    }


def get_question_by_id(question_id: str) -> dict:
    """
    Get a specific question by ID.
    """
    question = questions_collection.find_one({"_id": question_id})
    if question:
        return {
            "id": question["_id"],
            "title": question["title"],
            "description": question["description"],
            "created_at": question["created_at"],
            "likes": question["likes"],
            "dislikes": question["dislikes"],
            "tags": question["tags"],
            "difficulty": question["difficulty"],
            "status": question["status"],
            "hints": question.get("hints", []),
            "skills": question.get("learning_objectives", []),
            "categories": question.get("categories", [])
        }
    return None
