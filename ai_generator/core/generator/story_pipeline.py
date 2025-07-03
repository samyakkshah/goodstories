from typing import Dict, Any, Union
from core.generator.agents.extract_characters_agent import (
    extract_character_data,
    extract_new_character_data,
)
from core.generator.agents.metadata_extraction_agent import extract_story_metadata
from core.generator.agents.sketchboard_agent import (
    generate_sketchboard,
    generate_sketchboard_for_continuation,
)
from core.generator.agents.story_prompt_agent import (
    generate_draft_story,
    generate_draft_story_for_continuation,
)
from core.generator.agents.critique_agent import (
    critique_draft_for_continuation,
    critique_draft_story,
)
from core.generator.agents.final_story_agent import (
    generate_final_story,
    generate_final_story_for_continuation,
)

from core.generator.agents.image_generator_prompt_agent import generate_image_prompt
from core.constants.helper import random_genre, random_tone
from utilities.supabase_helper import save_characters_to_db


from typing import Tuple

from utilities.utils import (
    build_rich_context_string,
    extract_and_save_new_relationships,
    is_semantically_in_range,
    load_comprehensive_context,
    load_story_continuity_rules,
    save_story_critique,
    update_character_emotional_progression,
    format_continuity_rules_for_prompt,
    update_story_state_after_page,
    get_context_changes,
)


def generate_full_story_pipeline(
    model_used: str = "llama3",
) -> Tuple[Dict[str, Any], Any, str, str, str]:
    genre = random_genre()
    tone = random_tone()

    # Step 1: Sketchboard
    sketch = generate_sketchboard(genre, tone, model_name=model_used)
    print(sketch)

    try:
        character_data = extract_character_data(sketch)
        print(character_data)
    except:
        character_data = {}
        print("Error in JSON Format")
    # Step 2: First Draft
    draft = generate_draft_story(sketch_text=sketch, model_used=model_used)
    print(draft)
    # Step 3: Critique
    critique = critique_draft_story(
        draft_text=draft, sketch=sketch, model_used=model_used
    )

    print(critique)

    # Step 4: Final Story
    final = generate_final_story(
        genre=", ".join(genre),
        tone=tone,
        sketch_text=sketch,
        draft_text=draft,
        critique_text=critique,
        model_used=model_used,
    )

    extracted_metadata = extract_story_metadata(sketch, final["content"])
    final["metadata"].update(extracted_metadata)

    image_prompt = generate_image_prompt(sketch, final["content"])
    return final, character_data, sketch, critique, image_prompt


def generate_next_page_pipeline(
    story: dict, last_page: dict, character_context: str, model: str = "llama3"
) -> dict:

    context = load_comprehensive_context(story["story_id"], last_page["page_number"])
    rich_context_str = build_rich_context_string(context)

    sketch = generate_sketchboard_for_continuation(
        story, last_page, rich_context_str, model=model
    )

    print(sketch)

    try:
        character_data = extract_new_character_data(sketch)
        print(character_data)
    except:
        character_data = []
        print("Error in JSON Format")

    update_character_emotional_progression(story["story_id"], sketch)
    for character in character_data:
        extract_and_save_new_relationships(story["story_id"], character, sketch)

    rules = load_story_continuity_rules(story["story_id"])
    rules_text = format_continuity_rules_for_prompt(rules)

    draft = ""
    attempt = 1
    while True:
        draft = generate_draft_story_for_continuation(
            sketch, last_page["content"], rules_text, model=model
        )
        if is_semantically_in_range(last_page["content"], draft, lt=0.7, ut=0.89):
            break
        print(f"Attempt {attempt+1}: Similar to last page, retrying...")
        attempt += 1

    print(draft)

    critique = critique_draft_for_continuation(draft, last_page["content"], model=model)
    print(critique)

    save_story_critique(
        story["story_id"],
        last_page["page_number"] + 1,
        critique_type="continuity",
        critique_content=critique,
        suggested_improvements=[],
        severity_level=2,
    )

    max_retries = 2
    final = {"content": draft}
    for attempt in range(max_retries + 1):
        final = generate_final_story_for_continuation(
            context=last_page["content"],
            draft_text=draft,
            critique_text=critique,
            character_context=rich_context_str,
            model=model,
        )
        if is_semantically_in_range(draft, final["content"], lt=0.83, ut=0.92):
            break
        print(f"Attempt {attempt+1}: Different from draft, retrying...")

    metadata = extract_story_metadata(sketch, final["content"])
    final.update(metadata)
    update_story_state_after_page(
        story["story_id"], last_page["page_number"] + 1, final["content"], sketch
    )

    context_changes = get_context_changes(
        story["story_id"], last_page["page_number"] + 1
    )

    return {
        "content": final["content"],
        "metadata": final,  # includes prompt, version, etc.
        "new_characters": character_data,
        "context_updates": context_changes,
    }
