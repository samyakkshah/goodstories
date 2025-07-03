from typing import Any, Dict, Optional
from sentence_transformers import SentenceTransformer, util

from core.generator.agents.event_extraction_agent import extract_story_events_from_text
from core.supabase_client import get_supabase_client
from utilities.supabase_helper import (
    get_current_location,
    get_story_summary,
    get_unresolved_conflicts,
    get_all_character_current_states,
    get_relationship_issues,
    get_recent_story_events,
    get_mood_timeline,
)

similarity_model = SentenceTransformer("all-MiniLM-L6-v2")  # light + fast


def is_semantically_in_range(
    text1: str, text2: str, lt: float = 0.75, ut: float = 0.92
) -> bool:
    emb1 = similarity_model.encode(text1, convert_to_tensor=True)
    emb2 = similarity_model.encode(text2, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(emb1, emb2).item()
    print(f"Similarity score: {similarity:.4f}")
    return lt < similarity < ut


def load_comprehensive_context(story_id: str, page_number: int) -> Dict[str, Any]:
    """Load all relevant context for story continuation."""
    try:
        context = {
            "story_summary": get_story_summary(story_id),
            "current_location": get_current_location(story_id, page_number),
            "active_conflicts": get_unresolved_conflicts(story_id),
            "character_states": get_all_character_current_states(story_id),
            "recent_events": get_recent_story_events(story_id, last_n_pages=3),
            "relationship_tensions": get_relationship_issues(story_id),
            "mood_progression": get_mood_timeline(story_id),
        }
        return context
    except Exception as e:
        print(f"Error loading context: {e}")
        return {}


def build_rich_context_string(context: Dict[str, Any]) -> str:
    """Convert context dictionary to formatted string for LLM prompts."""
    context_parts = []

    if context.get("story_summary"):
        context_parts.append(f"STORY OVERVIEW:\n{context['story_summary']}")

    if context.get("current_location"):
        context_parts.append(f"CURRENT LOCATION: {context['current_location']}")

    if context.get("active_conflicts"):
        conflicts_str = "\n- ".join(context["active_conflicts"])
        context_parts.append(f"ACTIVE CONFLICTS:\n- {conflicts_str}")

    if context.get("character_states"):
        char_states = []
        for name, state in context["character_states"].items():
            char_info = (
                f"{name}: {state.get('emotional_state', 'unknown')} emotional state"
            )
            if state.get("desire"):
                char_info += f", wants {state['desire']}"
            if state.get("last_action"):
                char_info += f", last did: {state['last_action']}"
            char_states.append(char_info)
        context_parts.append(f"CHARACTER STATES:\n- " + "\n- ".join(char_states))

    if context.get("recent_events"):
        events_str = []
        for event in context["recent_events"][:5]:  # Last 5 events
            events_str.append(f"Page {event['page']}: {event['description']}")
        if events_str:
            context_parts.append(f"RECENT EVENTS:\n- " + "\n- ".join(events_str))

    if context.get("relationship_tensions"):
        tensions = []
        for tension in context["relationship_tensions"][:3]:  # Top 3 tensions
            tensions.append(
                f"{tension['type']} relationship issues: {', '.join(tension['issues'][:2])}"
            )
        if tensions:
            context_parts.append(f"RELATIONSHIP TENSIONS:\n- " + "\n- ".join(tensions))

    if context.get("mood_progression"):
        context_parts.append(f"MOOD PROGRESSION: {context['mood_progression']}")

    return "\n\n".join(context_parts)


import re
from typing import List


def extract_location_from_sketch(sketch: str) -> str:
    """Extract location from sketchboard text."""
    patterns = [
        r"Location[:\s]*([^\n]+)",
        r"Setting[:\s]*([^\n]+)",
        r"Where[:\s]*([^\n]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, sketch, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


def extract_conflicts_from_sketch(sketch: str) -> List[str]:
    """Extract conflicts from sketchboard text."""
    conflicts = []

    # Look for conflict sections
    conflict_patterns = [
        r"conflict[:\s]*([^\n]+)",
        r"tension[:\s]*([^\n]+)",
        r"problem[:\s]*([^\n]+)",
    ]

    for pattern in conflict_patterns:
        matches = re.findall(pattern, sketch, re.IGNORECASE)
        conflicts.extend([match.strip() for match in matches])

    return conflicts[:3]  # Limit to top 3


def extract_mood_from_sketch(sketch: str) -> str:
    """Extract mood/atmosphere from sketchboard."""
    patterns = [
        r"Tone[:\s]*([^\n]+)",
        r"Mood[:\s]*([^\n]+)",
        r"Atmosphere[:\s]*([^\n]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, sketch, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


def extract_theme_from_sketch(sketch: str) -> str:
    """Extract main theme from sketchboard."""
    patterns = [
        r"Theme[:\s]*([^\n]+)",
        r"main point[:\s]*([^\n]+)",
        r"story about[:\s]*([^\n]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, sketch, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


def extract_emotional_state(sketch: str, character_name: str) -> str:
    """Extract character's emotional state from sketch."""
    # Look for character name followed by emotional descriptors
    pattern = rf"{re.escape(character_name)}[^\n]*?(?:feels?|is|becomes?)\s+([^,.\n]+)"
    match = re.search(pattern, sketch, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Look for general emotional descriptors
    emotional_words = [
        "angry",
        "sad",
        "happy",
        "confused",
        "determined",
        "fearful",
        "hopeful",
        "desperate",
    ]
    for word in emotional_words:
        if word in sketch.lower() and character_name.lower() in sketch.lower():
            return word

    return "uncertain"


def extract_time_context_from_sketch(sketch: str) -> str:
    patterns = [r"Time[:\s]*([^\n]+)", r"Era[:\s]*([^\n]+)", r"When[:\s]*([^\n]+)"]
    for pattern in patterns:
        match = re.search(pattern, sketch, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


def extract_foreshadowing_from_sketch(sketch: str) -> list:
    matches = re.findall(r"Foreshadowing[:\s]*([^\n]+)", sketch, re.IGNORECASE)
    return [m.strip() for m in matches] if matches else []


def extract_pacing_notes_from_sketch(sketch: str) -> str:
    match = re.search(r"Pacing[:\s]*([^\n]+)", sketch, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def extract_unresolved_tensions_from_sketch(sketch: str) -> list:
    matches = re.findall(r"Tension[:\s]*([^\n]+)", sketch, re.IGNORECASE)
    return [m.strip() for m in matches] if matches else []


def extract_story_events(content: str, page_number: int) -> List[Dict[str, Any]]:
    """Extract key events from story content."""
    try:
        events = extract_story_events_from_text(content)
        for event in events:
            event["page_number"] = page_number
        return events
    except Exception as e:
        print(f"Error extracting structured events: {e}")
        return []


def save_story_context(
    story_id: str, page_number: int, sketch: str, content: str = ""
) -> bool:
    """Save story context to database."""
    try:
        supabase = get_supabase_client()

        context_data = {
            "story_id": story_id,
            "page_number": page_number,
            "current_location": extract_location_from_sketch(sketch),
            "time_context": extract_time_context_from_sketch(sketch),
            "active_conflicts": extract_conflicts_from_sketch(sketch),
            "unresolved_tensions": extract_unresolved_tensions_from_sketch(sketch),
            "foreshadowing_elements": extract_foreshadowing_from_sketch(sketch),
            "mood_atmosphere": extract_mood_from_sketch(sketch),
            "pacing_notes": extract_pacing_notes_from_sketch(sketch),
        }

        result = supabase.table("story_context").upsert(context_data).execute()
        return result.data is not None
    except Exception as e:
        print(f"Error saving story context: {e}")
        return False


def save_story_events(story_id: str, page_number: int, content: str) -> bool:
    """Save story events to database."""
    try:
        events = extract_story_events(content, page_number)
        print(f"Events: {events}")
        if not events:
            return True
        supabase = get_supabase_client()

        character_result = (
            supabase.table("story_characters")
            .select("character_id, name")
            .eq("story_id", story_id)
            .execute()
        )

        character_map = (
            {c["name"]: c["character_id"] for c in character_result.data}
            if character_result.data
            else {}
        )

        for event in events:
            name_list = event.get("characters_involved", [])
            uuid_list = [
                character_map.get(name) for name in name_list if name in character_map
            ]
            event["characters_involved"] = uuid_list
            event["story_id"] = story_id

        result = supabase.table("story_events").insert(events).execute()
        return result.data is not None
    except Exception as e:
        print(f"Error saving story events: {e}")
        return False


def update_character_emotional_progression(story_id: str, sketch: str) -> bool:
    """Update character emotional states based on sketch."""
    try:
        supabase = get_supabase_client()

        # Get existing characters
        characters = (
            supabase.table("story_characters")
            .select("character_id, name")
            .eq("story_id", story_id)
            .execute()
        )

        if not characters.data:
            return True

        for char in characters.data:
            new_emotional_state = extract_emotional_state(sketch, char["name"])
            if new_emotional_state and new_emotional_state != "uncertain":
                update_data = {
                    "current_emotional_state": new_emotional_state,
                    "character_arc_stage": determine_arc_stage(sketch, char["name"]),
                }

                supabase.table("story_characters").update(update_data).eq(
                    "character_id", char["character_id"]
                ).execute()

        return True
    except Exception as e:
        print(f"Error updating character progression: {e}")
        return False


def determine_arc_stage(sketch: str, character_name: str) -> str:
    """Determine character arc stage from sketch content."""
    sketch_lower = sketch.lower()
    name_lower = character_name.lower()

    if "realizes" in sketch_lower and name_lower in sketch_lower:
        return "realization"
    elif "confronts" in sketch_lower and name_lower in sketch_lower:
        return "confrontation"
    elif "decides" in sketch_lower and name_lower in sketch_lower:
        return "decision"
    elif "changes" in sketch_lower and name_lower in sketch_lower:
        return "transformation"
    else:
        return "development"


def save_story_critique(
    story_id: str,
    page_number: int,
    critique_type: str,
    critique_content: str,
    suggested_improvements: Optional[list],
    severity_level: int = 2,
) -> bool:
    """
    Save a single critique entry to the story_critique table.
    """
    try:
        supabase = get_supabase_client()

        data = {
            "story_id": story_id,
            "page_number": page_number,
            "critique_type": critique_type,
            "critique_content": critique_content,
            "suggested_improvements": suggested_improvements or [],
            "severity_level": severity_level,
            "is_resolved": False,
        }

        result = supabase.table("story_critique").insert(data).execute()
        return result.data is not None

    except Exception as e:
        print(f"Error saving critique: {e}")
        return False


def save_initial_relationships(story_id: str, character_data: Dict) -> bool:
    """
    Save any extracted relationships (including main-main) after characters are saved.
    """
    try:
        if not character_data.get("relationships"):
            return True

        supabase = get_supabase_client()

        # Fetch all characters with IDs
        res = (
            supabase.table("story_characters")
            .select("character_id, name")
            .eq("story_id", story_id)
            .execute()
        )
        if not res.data:
            return False

        char_map = {c["name"]: c["character_id"] for c in res.data}

        relationships = []
        for rel in character_data["relationships"]:
            c1_id = char_map.get(rel["character_1_name"])
            c2_id = char_map.get(rel["character_2_name"])
            if c1_id and c2_id:
                relationships.append(
                    {
                        "story_id": story_id,
                        "character_1_id": c1_id,
                        "character_2_id": c2_id,
                        "relationship_type": rel.get(
                            "relationship_type", "unspecified"
                        ),
                        "relationship_strength": 5,
                        "relationship_status": "developing",
                    }
                )

        if relationships:
            supabase.table("character_relationships").insert(relationships).execute()

        return True

    except Exception as e:
        print(f"Error saving initial relationships: {e}")
        return False


def extract_and_save_new_relationships(
    story_id: str, new_characters: Dict, sketch: str
) -> bool:
    """Extract and save new character relationships."""
    try:
        if not new_characters.get("new_characters"):
            return True

        supabase = get_supabase_client()

        # Get existing characters
        existing_chars = (
            supabase.table("story_characters")
            .select("character_id, name")
            .eq("story_id", story_id)
            .execute()
        )
        existing_char_map = (
            {char["name"]: char["character_id"] for char in existing_chars.data}
            if existing_chars.data
            else {}
        )

        relationships = []
        for new_char in new_characters["new_characters"]:
            if new_char.get("relationship_to_main"):
                # Find main character
                main_chars = (
                    [char for char in existing_chars.data if char.get("is_main")]
                    if existing_chars.data
                    else []
                )
                if main_chars:
                    relationships.append(
                        {
                            "story_id": story_id,
                            "character_1_id": main_chars[0]["character_id"],
                            "character_2_id": new_char.get(
                                "character_id"
                            ),  # Assuming this is set
                            "relationship_type": new_char["relationship_to_main"],
                            "relationship_strength": 5,  # Default
                            "relationship_status": "developing",
                        }
                    )

        if relationships:
            result = (
                supabase.table("character_relationships")
                .insert(relationships)
                .execute()
            )
            return result.data is not None

        return True
    except Exception as e:
        print(f"Error saving relationships: {e}")
        return False


def update_story_state_after_page(
    story_id: str, page_number: int, content: str, sketch: str = ""
) -> Dict[str, bool]:
    """Update all story state after page generation."""
    results = {
        "context_saved": False,
        "events_saved": False,
        "characters_updated": False,
    }

    if sketch:
        results["context_saved"] = save_story_context(
            story_id, page_number, sketch, content
        )
        results["characters_updated"] = update_character_emotional_progression(
            story_id, sketch
        )

    results["events_saved"] = save_story_events(story_id, page_number, content)

    return results


def load_story_continuity_rules(story_id: str) -> List[Dict[str, Any]]:
    """Load active continuity rules for story."""
    try:
        supabase = get_supabase_client()
        result = (
            supabase.table("story_continuity")
            .select("rule_type, rule_description, priority_level")
            .eq("story_id", story_id)
            .eq("is_active", True)
            .order("priority_level")
            .execute()
        )

        if result.data:
            return result.data
        return []
    except Exception as e:
        print(f"Error loading continuity rules: {e}")
        return []


def save_continuity_rule(
    story_id: str, rule_type: str, rule_description: str, priority: int = 2
) -> bool:
    """Save a new continuity rule."""
    try:
        supabase = get_supabase_client()

        rule_data = {
            "story_id": story_id,
            "rule_type": rule_type,
            "rule_description": rule_description,
            "priority_level": priority,
            "is_active": True,
        }

        result = supabase.table("story_continuity").insert(rule_data).execute()
        return result.data is not None
    except Exception as e:
        print(f"Error saving continuity rule: {e}")
        return False


def format_continuity_rules_for_prompt(rules: List[Dict]) -> str:
    """Format continuity rules for LLM prompt."""
    if not rules:
        return ""

    formatted_rules = []

    high_priority = [r for r in rules if r.get("priority_level", 2) == 1]
    medium_priority = [r for r in rules if r.get("priority_level", 2) == 2]

    if high_priority:
        formatted_rules.append("CRITICAL CONTINUITY RULES (MUST FOLLOW):")
        for rule in high_priority:
            formatted_rules.append(f"- {rule['rule_description']}")

    if medium_priority:
        formatted_rules.append("\nIMPORTANT CONTINUITY RULES:")
        for rule in medium_priority[:5]:  # Limit to top 5
            formatted_rules.append(f"- {rule['rule_description']}")

    return "\n".join(formatted_rules)


def auto_generate_continuity_rules(story_id: str, character_data: Dict) -> bool:
    """Auto-generate basic continuity rules from character data."""
    try:
        rules_created = 0

        # Character personality rules
        for char_type in ["main_characters", "secondary_characters"]:
            if char_type in character_data:
                for char in character_data[char_type]:
                    if char.get("personality_traits"):
                        rule_desc = f"{char['name']} is {', '.join(char['personality_traits'][:2])} - maintain these traits"
                        if save_continuity_rule(
                            story_id, "character_trait", rule_desc, priority=1
                        ):
                            rules_created += 1

                    if char.get("core_desire"):
                        rule_desc = f"{char['name']} wants {char['core_desire']} - this drives their actions"
                        if save_continuity_rule(
                            story_id, "character_motivation", rule_desc, priority=1
                        ):
                            rules_created += 1

        print(f"Auto-generated {rules_created} continuity rules")
        return rules_created > 0
    except Exception as e:
        print(f"Error auto-generating rules: {e}")
        return False


def get_context_changes(story_id: str, page_number: int) -> Dict[str, Any]:
    """Get what changed in the latest page."""
    try:
        supabase = get_supabase_client()

        # Get current and previous context
        current = (
            supabase.table("story_context")
            .select("*")
            .eq("story_id", story_id)
            .eq("page_number", page_number)
            .single()
            .execute()
        )
        previous = (
            supabase.table("story_context")
            .select("*")
            .eq("story_id", story_id)
            .eq("page_number", page_number - 1)
            .single()
            .execute()
        )

        changes = {}

        if current.data and previous.data:
            current_data = current.data
            previous_data = previous.data

            # Check location change
            if current_data.get("current_location") != previous_data.get(
                "current_location"
            ):
                changes["location_changed"] = {
                    "from": previous_data.get("current_location"),
                    "to": current_data.get("current_location"),
                }

            # Check mood change
            if current_data.get("mood_atmosphere") != previous_data.get(
                "mood_atmosphere"
            ):
                changes["mood_changed"] = {
                    "from": previous_data.get("mood_atmosphere"),
                    "to": current_data.get("mood_atmosphere"),
                }

        return changes
    except Exception as e:
        print(f"Error getting context changes: {e}")
        return {}


def save_initial_story_context(
    story_id: str, sketch: str, content: str, character_data: Dict
) -> bool:
    """Save initial story context and generate continuity rules."""
    try:
        # Save story context
        context_saved = save_story_context(story_id, 1, sketch, content)

        # Save story events
        events_saved = save_story_events(story_id, 1, content)

        # Auto-generate continuity rules
        rules_generated = auto_generate_continuity_rules(story_id, character_data)

        print(
            f"Initial context saved: {context_saved}, Events: {events_saved}, Rules: {rules_generated}"
        )
        return context_saved and events_saved
    except Exception as e:
        print(f"Error saving initial context: {e}")
        return False
