from typing import List
from core.constants.helper import fetch_random_names
from core.generator.llm.ollama_llm import get_ollama
from core.generator.prompt.sketchboard import (
    sketchboard_prompt,
    sketchboard_prompt_for_continuation,
)
from langchain_core.output_parsers import StrOutputParser


def generate_sketchboard(
    genre: List[str], tone: str, model_name: str = "gemma3:12b"
) -> str:
    names = fetch_random_names()
    llm = get_ollama(
        model=model_name, temperature=2, verbose=False, top_k=30, top_p=0.9
    )
    prompt = sketchboard_prompt()
    chain = prompt | llm | StrOutputParser()
    sketch_text = chain.invoke(
        {"genre": ", ".join(genre), "tone": tone, "names": ", ".join(names)}
    )
    return sketch_text.strip()


def generate_sketchboard_for_continuation(
    story: dict,
    last_page: dict,
    character_context: str,
    model: str = "gemma3:12b",
) -> str:
    names = fetch_random_names(2)
    llm = get_ollama(
        model=model, temperature=0.9, verbose=False, top_k=35, num_ctx=10000
    )
    prompt = sketchboard_prompt_for_continuation()
    chain = prompt | llm | StrOutputParser()
    sketch_text = chain.invoke(
        {
            "genre": story.get("genre", ""),
            "tone": story.get("tone", ""),
            "context": last_page["content"],
            "character_context": character_context,
            "names": ", ".join(names),
        }
    )
    return sketch_text.strip()
