from typing import List
from uuid import UUID
from fastapi import APIRouter, Query
from schemas.story import FullStoryOut, StoryOut
from services.story_service import (
    generate_and_store_next_page,
    generate_and_store_stories,
)

story_router = APIRouter()


@story_router.post("/stories/generate", response_model=List[StoryOut])
def generate_stories(count: int = Query(5, ge=1, le=20)):
    """
    Generate and store AI-generated stories using Ollama + LangChain.
    Defaults to 5 stories. Max 20.
    """
    return generate_and_store_stories(count)



@story_router.get("/stories/generate/new_page/{story_id}", response_model=str)
def generate_new_page_for_story(story_id: UUID):
    return generate_and_store_next_page(story_id)
