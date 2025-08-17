from langchain_core.documents import Document
from app.pipelines.daily_question_pipeline import daily_question_chain
from app.llm.provider import invoke_with_retries
from app.config.vectorestore import ChromaDB

#TODO: Make this configurable
# This is the default user prompt for generating a daily question.
DEFAULT_USER_PROMPT = "Generate a daily question for a full stack developer working on microservices."

def generate_daily_question() -> str:
    """Generate a daily question using the LLM pipeline."""
    payload = {"user_question": DEFAULT_USER_PROMPT}
    response = invoke_with_retries(daily_question_chain, payload)
    # ChatHuggingFace returns an AIMessage by default; str() yields content.
    return str(response.content) if hasattr(response, "content") else str(response)

def add_daily_question_to_store(question: str) -> None:
    """Add a daily question to the ChromaDB collection."""
    chroma_store = ChromaDB(collection="daily_questions")
    doc = Document(page_content=question, metadata={})
    chroma_store.add_documents([doc])
