from datetime import datetime, timezone, timedelta
from uuid import UUID

from fastapi import HTTPException
from core.generator.agents.continuation_agent import generate_next_page_text
from core.generator.image_pipeline import generate_and_upload_cover_image_to_supabase
from core.generator.prompt.continuation import continuation_prompt
from core.generator.story_pipeline import (
    generate_full_story_pipeline,
    generate_next_page_pipeline,
)
from core.supabase_client import get_supabase_client, get_supabase_service
from schemas.story import StoryOut, StoryPageOut

from typing import List, Optional

from utilities.supabase_helper import (
    get_character_prompt_block,
    get_latest_story_page,
    save_characters_to_db,
    save_new_characters_to_db,
)
from utilities.utils import (
    save_initial_relationships,
    save_initial_story_context,
    save_story_critique,
)

# New Funcs


def add_page_to_story(
    story_id: UUID,
    content: str,
    prompt: str,
    page_number: int,
    summary: Optional[str] = None,
    model_used: str = "llama3",
) -> StoryPageOut:
    supabase = get_supabase_client()
    page = {
        "story_id": str(story_id),
        "page_number": page_number,
        "content": content,
        "generation_prompt": prompt,
        "model_used": model_used,
        "page_summary": summary,
        "version_number": 1,
        "is_final_version": True,
    }

    res = supabase.table("story_pages").insert(page).execute()

    if not res.data:
        raise HTTPException(status_code=500, detail="Page insert failed")

    # Update current_page_number and current_status
    supabase.table("stories").update(
        {"current_page_number": page_number, "current_status": summary}
    ).eq("story_id", str(story_id)).execute()

    return StoryPageOut(**res.data[0])


def get_last_n_pages(story_id: UUID, n: int = 2) -> List[StoryPageOut]:
    supabase = get_supabase_client()

    res = (
        supabase.table("story_pages")
        .select("*")
        .eq("story_id", str(story_id))
        .order("page_number", desc=True)
        .limit(n)
        .execute()
    )

    return [StoryPageOut(**page) for page in reversed(res.data)]


def generate_and_store_stories(count: int = 10) -> List[StoryOut]:
    supabase = get_supabase_client()
    supabase_service = get_supabase_service()
    results = []

    for _ in range(count):
        res, character_data, sketch, critique, prompt = generate_full_story_pipeline()
        story_data = res["metadata"]
        page_1_content = res["content"]

        story_data["created_at"] = datetime.now(timezone.utc).isoformat()

        story_res = supabase.table("stories").insert(story_data).execute()

        if not story_res.data:
            continue

        story_id = story_res.data[0]["story_id"]

        cover_image_url = generate_and_upload_cover_image_to_supabase(
            prompt_text=prompt,
            supabase_client=supabase_service,
            bucket_name="cover-image",
            story_id=story_id,
        )

        supabase.table("stories").update({"cover_image_url": cover_image_url}).eq(
            "story_id", story_id
        ).execute()

        save_characters_to_db(
            story_id,
            character_data["main_characters"],
            character_data["secondary_characters"],
        )

        save_initial_story_context(story_id, sketch, res["content"], character_data)
        save_initial_relationships(story_id, character_data)
        save_story_critique(
            story_id,
            page_number=1,
            critique_type="continuity",
            critique_content=critique,
            suggested_improvements=[],
            severity_level=2,
        )
        page_data = {
            "story_id": story_id,
            "page_number": 1,
            "content": page_1_content,
            "generation_prompt": story_data.get("seed_prompt", ""),
            "model_used": story_data.get("model_used", "llama3"),
            "version_number": 1,
            "is_final_version": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        supabase.table("story_pages").insert(page_data).execute()

        results.append(StoryOut(**story_res.data[0]))

    return results


def generate_and_store_next_page(story_id: UUID) -> str:
    supabase = get_supabase_client()
    story = (
        supabase.table("stories")
        .select("*")
        .eq("story_id", str(story_id))
        .single()
        .execute()
        .data
    )
    last_page = get_latest_story_page(story_id)
    character_context = get_character_prompt_block(story_id)

    result = generate_next_page_pipeline(story, last_page, character_context)
    new_characters = result.get("new_characters", [])
    next_page_number = last_page["page_number"] + 1

    supabase.table("story_pages").insert(
        {
            "story_id": str(story_id),
            "page_number": next_page_number,
            "content": result["content"],
            "generation_prompt": result["metadata"]["generation_prompt"],
            "model_used": story.get("model_used", "llama3"),
            "version_number": 1,
            "is_final_version": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    ).execute()

    update_data = {
        "current_page_number": next_page_number,
        "current_status": None,
        "is_final_page": False,
    }

    # Add new metadata fields if present
    for field in [
        "main_theme",
        "central_conflict",
        "target_age_group",
        "emotional_arc",
        "story_summary",
        "last_emotional_state",
        "next_planned_direction",
    ]:
        if result["metadata"].get(field):
            update_data[field] = result["metadata"][field]

    # Update stories table
    supabase.table("stories").update(update_data).eq(
        "story_id", str(story_id)
    ).execute()

    if len(new_characters) > 0:
        save_new_characters_to_db(story_id=story_id, new_chars=new_characters)

    return result["content"]


def start_of_today_utc():
    now = datetime.now(timezone.utc)
    return now.replace(hour=0, minute=0, second=0, microsecond=0)
