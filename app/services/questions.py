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

def add_daily_question_to_mongodb(question: dict) -> None:
    """Add a daily question to the MongoDB collection."""
    question_document = {
        "_id": f"q_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "title": question.get("title", ""),  # Extract title from question
        "description": question.get("description", ""),  # Extract description from question
        "created_at": datetime.utcnow().isoformat(),
        "likes": 0,
        "dislikes": 0,
        "hints": question.get("hints", []),
        "tags": question.get("tags", []),
        "difficulty": question.get("difficulty", "None"),
        "status": "published"
    }
    questions_collection.insert_one(question_document)

def add_tech_description_to_store(description: str, metadata: TechDescriptionMetadata) -> None:
    """Add a tech description to the ChromaDB collection."""
    doc_id = str(uuid.uuid4())
    doc = Document(id=doc_id, page_content=description, metadata=metadata.model_dump())
    chroma_db.add_documents(collection="tech_description",documents=[doc])

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
        }
    return None
