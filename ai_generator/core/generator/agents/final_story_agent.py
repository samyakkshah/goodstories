from typing import Dict, List
from langchain_core.output_parsers import StrOutputParser
from core.generator.agents.metadata_extraction_agent import extract_story_metadata
from core.generator.agents.title_agent import generate_title
from core.generator.llm.ollama_llm import get_ollama
from core.generator.prompt.final_story import (
    final_continuation_prompt,
    final_story_prompt,
)


def generate_final_story(
    genre: str,
    tone: str,
    sketch_text: str,
    draft_text: str,
    critique_text: str,
    model_used: str = "gemma3",
) -> dict:
    try:
        llm = get_ollama(
            model=model_used,
            temperature=0.9,
            verbose=False,
            top_k=30,
            top_p=0.8,
            num_ctx=10000,
        )
    except:
        llm = get_ollama(model="llama3")

    prompt = final_story_prompt()
    chain = prompt | llm | StrOutputParser()

    final_story = chain.invoke(
        {"sketch": sketch_text, "draft": draft_text, "critique": critique_text}
    ).strip()

    # Try extracting title, genre, tone from sketch if present
    title = generate_title(final_story)

    story_metadata = {
        "title": title.strip('"') or final_story[:100].split(".")[0],
        "genre": genre,
        "tone": tone,
        "tags": [genre, tone] if genre and tone else [],
        "chapter_number": 1,
        "current_page_number": 1,
        "story_type": "short",
        "model_used": model_used,
        "seed_prompt": prompt.format(
            sketch=sketch_text, draft=draft_text, critique=critique_text
        ),
        "current_status": None,  # You can optionally add a summary agent here
        "is_final_page": False,
        "is_final_chapter": False,
    }

    return {"metadata": story_metadata, "content": final_story}


def extract_field_from_sketch(field: str, sketch: str) -> str:
    for line in sketch.splitlines():
        if line.lower().startswith(f"{field.lower()}:"):
            return line.split(":", 1)[1].strip()
    return ""


def generate_final_story_for_continuation(
    context: str,
    draft_text: str,
    critique_text: str,
    character_context: str,
    model: str = "gemma3",
) -> dict:
    try:
        llm = get_ollama(
            model=model,
            temperature=0.8,
            verbose=False,
            top_k=30,
            top_p=0.8,
            num_ctx=10000,
        )
    except:
        llm = get_ollama(model="llama3")

    prompt = final_continuation_prompt()
    chain = prompt | llm | StrOutputParser()

    final_story = chain.invoke(
        {
            "context": context,
            "draft": draft_text,
            "critique": critique_text,
            "character_context": character_context,
        }
    ).strip()
    return {
        "content": final_story,
        "generation_prompt": prompt.format(
            context=context,
            draft=draft_text,
            critique=critique_text,
            character_context=character_context,
        ),
    }
