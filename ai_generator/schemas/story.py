from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class StoryBase(BaseModel):
    title: str
    genre: Optional[str] = None
    tone: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    story_type: Optional[str] = "short"
    universe_id: Optional[UUID] = None
    chapter_number: Optional[int] = 1
    current_page_number: Optional[int] = 1
    current_status: Optional[str] = None
    is_final_page: Optional[bool] = False
    is_final_chapter: Optional[bool] = False
    next_universe_id: Optional[UUID] = None
    model_used: Optional[str] = None
    seed_prompt: Optional[str] = None


class StoryPageBase(BaseModel):
    story_id: UUID
    page_number: int
    content: str
    is_final_version: bool = True
    generation_prompt: Optional[str] = None
    model_used: Optional[str] = None
    version_number: int = 1
    page_summary: Optional[str] = None


class StoryCreate(StoryBase):
    pass


class StoryOut(StoryBase):
    story_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class StoryPageCreate(StoryPageBase):
    pass


class StoryPageOut(StoryPageBase):
    page_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class FullStoryOut(BaseModel):
    metadata: StoryOut
    pages: List[StoryPageOut]
