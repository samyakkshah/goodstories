from typing import List, Dict
from uuid import UUID
from datetime import datetime, timezone
from core.supabase_client import get_supabase_client


def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def save_characters_to_db(
    story_id: UUID, main_chars: List[Dict], secondary_chars: List[Dict]
):
    supabase = get_supabase_client()

    character_rows = []

    # Main character (only one)
    for char in main_chars:
        character_rows.append(
            {
                "story_id": str(story_id),
                "name": char["name"],
                "age": safe_int(char.get("age")),
                "role": char.get("role"),
                "relationship": None,
                "description": f"Desire: {char.get('core_desire')}, Fear: {char.get('deepest_fear')}, Status: {char.get('current_status')}",
                "is_main": True,
                "core_desire": char.get("core_desire"),
                "deepest_fear": char.get("deepest_fear"),
                "current_emotional_state": char.get("current_emotional_state", ""),
                "character_arc_stage": char.get("character_arc_stage", "introduction"),
                "last_action": char.get("last_action", ""),
                "motivation_evolution": char.get("motivation_evolution", ""),
                "personality_traits": char.get("personality_traits", []),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    # Secondary characters
    for char in secondary_chars:
        character_rows.append(
            {
                "story_id": str(story_id),
                "name": char["name"],
                "age": safe_int(char.get("age")),
                "role": char.get("role"),
                "relationship": char.get("relationship"),
                "description": char.get("description"),
                "is_main": False,
                "core_desire": char.get("core_desire"),
                "deepest_fear": char.get("deepest_fear"),
                "current_emotional_state": char.get("current_emotional_state", ""),
                "character_arc_stage": char.get("character_arc_stage", "introduction"),
                "last_action": char.get("last_action", ""),
                "motivation_evolution": char.get("motivation_evolution", ""),
                "personality_traits": char.get("personality_traits", []),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    # Insert all at once
    supabase.table("story_characters").insert(character_rows).execute()


def save_new_characters_to_db(story_id: UUID, new_chars: List[Dict]):
    supabase = get_supabase_client()

    character_rows = []

    # Main character (only one)
    for char in new_chars:
        character_rows.append(
            {
                "story_id": str(story_id),
                "name": char["name"],
                "age": safe_int(char.get("age")),
                "role": char.get("role"),
                "relationship": None,
                "description": f"Desire: {char.get('core_desire')}, Fear: {char.get('deepest_fear')}, Status: {char.get('current_status')}",
                "is_main": False,
                "core_desire": char.get("core_desire"),
                "deepest_fear": char.get("deepest_fear"),
                "current_emotional_state": char.get("current_emotional_state", ""),
                "character_arc_stage": char.get("character_arc_stage", "introduction"),
                "last_action": char.get("last_action", ""),
                "motivation_evolution": char.get("motivation_evolution", ""),
                "personality_traits": char.get("personality_traits", []),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    # Insert all at once
    supabase.table("story_characters").insert(character_rows).execute()


def get_character_prompt_block(story_id: UUID) -> str:
    supabase = get_supabase_client()
    response = (
        supabase.table("story_characters")
        .select("*")
        .eq("story_id", str(story_id))
        .execute()
    )
    if not response.data:
        return ""

    mains = []
    secondaries = []

    for char in response.data:
        line = f"{char['name']} ({char.get('age')}) - {char.get('role')}: {char.get('description')}"
        if char.get("is_main"):
            mains.append(f"- {line}")
        else:
            secondaries.append(f"- {line}")

    return f"""Main Characters:\n{chr(10).join(mains)}\n\nSecondary Characters:\n{chr(10).join(secondaries)}"""


def get_latest_story_page(story_id: UUID) -> dict:
    supabase = get_supabase_client()
    result = (
        supabase.table("story_pages")
        .select("*")
        .eq("story_id", str(story_id))
        .order("page_number", desc=True)
        .limit(1)
        .execute()
    )
    if not result.data:
        raise Exception("No pages found for this story.")
    return result.data[0]


from typing import Dict, List, Any, Optional
import json
from utilities.supabase_helper import get_supabase_client


def get_story_summary(story_id: str) -> str:
    """Get the main story summary and theme."""
    supabase = get_supabase_client()
    result = (
        supabase.table("stories")
        .select("story_summary, main_theme")
        .eq("story_id", story_id)
        .single()
        .execute()
    )
    if result.data:
        summary = result.data.get("story_summary", "")
        theme = result.data.get("main_theme", "")
        return f"Theme: {theme}\nSummary: {summary}" if theme and summary else ""
    return ""


def get_current_location(story_id: str, page_number: int) -> str:
    """Get the current story location."""
    supabase = get_supabase_client()
    result = (
        supabase.table("story_context")
        .select("current_location")
        .eq("story_id", story_id)
        .eq("page_number", page_number)
        .single()
        .execute()
    )
    if result.data:
        return result.data.get("current_location", "")
    return ""


def get_unresolved_conflicts(story_id: str) -> List[str]:
    """Get active conflicts that need resolution."""
    supabase = get_supabase_client()
    result = (
        supabase.table("story_context")
        .select("active_conflicts, unresolved_tensions")
        .eq("story_id", story_id)
        .order("page_number", desc=True)
        .limit(1)
        .execute()
    )
    if result.data:
        conflicts = result.data[0].get("active_conflicts", [])
        tensions = result.data[0].get("unresolved_tensions", [])
        return conflicts + tensions
    return []


def get_all_character_current_states(story_id: str) -> Dict[str, Dict]:
    """Get current emotional and motivational state of all characters."""
    supabase = get_supabase_client()
    result = (
        supabase.table("story_characters")
        .select(
            "name, current_emotional_state, core_desire, deepest_fear, character_arc_stage, last_action"
        )
        .eq("story_id", story_id)
        .execute()
    )

    characters = {}
    if result.data:
        for char in result.data:
            characters[char["name"]] = {
                "emotional_state": char.get("current_emotional_state", ""),
                "desire": char.get("core_desire", ""),
                "fear": char.get("deepest_fear", ""),
                "arc_stage": char.get("character_arc_stage", ""),
                "last_action": char.get("last_action", ""),
            }
    return characters


def get_recent_story_events(story_id: str, last_n_pages: int = 3) -> List[Dict]:
    """Get recent story events for context."""
    supabase = get_supabase_client()
    result = (
        supabase.table("story_events")
        .select("event_description, characters_involved, consequences, page_number")
        .eq("story_id", story_id)
        .order("page_number", desc=True)
        .limit(last_n_pages * 3)
        .execute()
    )

    events = []
    if result.data:
        for event in result.data:
            events.append(
                {
                    "description": event.get("event_description", ""),
                    "characters": event.get("characters_involved", []),
                    "consequences": event.get("consequences", []),
                    "page": event.get("page_number", 0),
                }
            )
    return events


def get_relationship_issues(story_id: str) -> List[Dict]:
    """Get unresolved relationship tensions."""
    supabase = get_supabase_client()
    result = (
        supabase.table("character_relationships")
        .select(
            "character_1_id, character_2_id, relationship_type, unresolved_issues, relationship_status"
        )
        .eq("story_id", story_id)
        .execute()
    )

    issues = []
    if result.data:
        for rel in result.data:
            if rel.get("unresolved_issues"):
                issues.append(
                    {
                        "characters": [
                            rel.get("character_1_id"),
                            rel.get("character_2_id"),
                        ],
                        "type": rel.get("relationship_type", ""),
                        "issues": rel.get("unresolved_issues", []),
                        "status": rel.get("relationship_status", ""),
                    }
                )
    return issues


def get_mood_timeline(story_id: str) -> str:
    """Get the emotional progression of the story."""
    supabase = get_supabase_client()
    result = (
        supabase.table("story_context")
        .select("mood_atmosphere, page_number")
        .eq("story_id", story_id)
        .order("page_number")
        .execute()
    )

    if result.data:
        moods = [
            f"Page {item['page_number']}: {item.get('mood_atmosphere', '')}"
            for item in result.data
            if item.get("mood_atmosphere")
        ]
        return " -> ".join(moods[-3:])  # Last 3 mood changes
    return ""
