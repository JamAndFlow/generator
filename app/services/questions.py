from langchain_core.documents import Document

from app.config.vectorestore import chroma_db
from app.llm.provider import invoke_with_retries
from app.pipelines.daily_question_pipeline import daily_question_chain


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

def add_tech_description_to_store(description: str, metadata: dict) -> None:
    """Add a tech description to the ChromaDB collection."""
    doc = Document(page_content=description, metadata=metadata)
    chroma_db.add_documents(collection="tech_description",documents=[doc])