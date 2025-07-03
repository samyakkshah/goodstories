from langchain_core.output_parsers import StrOutputParser
import random

from core.generator.llm.ollama_llm import get_ollama
from core.generator.prompt.story_draft import (
    story_draft_prompt,
    story_draft_prompt_for_continuation,
)


def generate_draft_story(sketch_text: str, model_used: str = "gemma3:12b") -> str:
    llm = get_ollama(
        model=model_used,
        temperature=1.5,
        verbose=False,
        top_k=40,
        top_p=0.8,
        num_ctx=10000,
    )
    prompt = story_draft_prompt()
    chain = prompt | llm | StrOutputParser()
    draft_text = chain.invoke({"sketch": sketch_text})
    return draft_text.strip()


def generate_draft_story_for_continuation(
    sketch_text: str, context: str, rules: str, model: str = "gemma3:12b"
) -> str:
    llm = get_ollama(
        model=model, temperature=1.5, verbose=False, top_k=50, top_p=0.95, num_ctx=10000
    )
    prompt = story_draft_prompt_for_continuation()
    chain = prompt | llm | StrOutputParser()
    draft_text = chain.invoke(
        {"sketch": sketch_text, "context": context, "rules": rules}
    )
    return draft_text.strip()
