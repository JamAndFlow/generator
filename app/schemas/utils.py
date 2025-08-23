from pydantic import BaseModel

class UserPrompt(BaseModel):
    """Schema for user prompt input."""
    user_prompt: str | None = None
