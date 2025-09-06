import time
from typing import Any, Dict

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from app.settings import settings


def build_chat_model() -> ChatHuggingFace:
    """Builds and returns a ChatHuggingFace model instance configured with the settings from the app."""
    llm = HuggingFaceEndpoint(
        repo_id=settings.LLM_REPO_ID,
        huggingfacehub_api_token=settings.HUGGINGFACEHUB_API_TOKEN,
        temperature=settings.LLM_TEMPERATURE,
        max_new_tokens=settings.LLM_MAX_NEW_TOKENS,
        timeout=settings.LLM_TIMEOUT_S,
    )
    return ChatHuggingFace(llm=llm)


# TODO: Improve this function
def invoke_with_retries(chain, payload: Dict[str, Any]):
    last_err = None
    for attempt in range(1, settings.LLM_RETRIES + 1):
        try:
            return chain.invoke(payload)
        except Exception as e:  # noqa: BLE001
            last_err = e
            # Exponential backoff with cap
            time.sleep(min(2**attempt, 8))
    raise RuntimeError(
        f"LLM invocation failed after {settings.LLM_RETRIES} attempts"
    ) from last_err
