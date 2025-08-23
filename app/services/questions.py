from langchain_core.documents import Document
from app.pipelines.daily_question_pipeline import daily_question_chain
from app.llm.provider import invoke_with_retries
from app.config.vectorestore import chroma_db
from app.config.database import questions_collection
from datetime import datetime

def generate_daily_question(user_prompt: str = None) -> str:
    """Generate a daily question using the LLM pipeline."""
    payload = {"user_prompt": user_prompt}
    response = invoke_with_retries(daily_question_chain, payload)
    # ChatHuggingFace returns an AIMessage by default; str() yields content.
    return str(response.content) if hasattr(response, "content") else str(response)

def add_daily_question_to_store(question: str) -> None:
    """Add a selected question to the ChromaDB collection."""
    doc = Document(page_content=question, metadata={})
    chroma_db.add_documents(collection="daily_questions",documents=[doc])

def add_daily_question_to_mongodb(question: str) -> None:
    """Add a daily question to the MongoDB collection."""
    question_document = {
        "_id": f"q_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "title": question.split("?")[0] + "?",  # Extract title from question
        "description": question,
        "created_at": datetime.utcnow().isoformat(),
        "likes": 0,
        "dislikes": 0,
        "hints": [],
        "tags": ["Daily", "Question"],
        "difficulty": "medium",
        "status": "published"
    }
    questions_collection.insert_one(question_document)

def add_tech_description_to_store(description: str, metadata: dict) -> None:
    """Add a tech description to the ChromaDB collection."""
    doc = Document(page_content=description, metadata=metadata)
    chroma_db.add_documents(collection="tech_description",documents=[doc])
