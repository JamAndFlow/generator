from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class UserPrompt(BaseModel):
    """Schema for user prompt input."""

    user_prompt: str | None = None


class TechDescriptionMetadata(BaseModel):
    """Schema for tech description metadata."""

    topic: str
    tech_stack: str
    difficulty: str
    tags: str


class TechDescription(BaseModel):
    """Schema for tech description input."""

    description: str
    metadata: TechDescriptionMetadata


class SortOrder(str, Enum):
    """Sort order enum."""
    ASC = "asc"
    DESC = "desc"


class QuestionFilters(BaseModel):
    """Schema for question list filters."""
    title: Optional[str] = None
    tags: Optional[List[str]] = None
    difficulty: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    page: int = Field(default=1, gt=0)
    per_page: int = Field(default=10, gt=0, le=100)
    sort_by: str = Field(default="created_at")
    sort_order: SortOrder = SortOrder.DESC
