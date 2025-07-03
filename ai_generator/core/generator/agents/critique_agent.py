from langchain_core.output_parsers import StrOutputParser
from core.generator.llm.ollama_llm import get_ollama
from core.generator.prompt.critique import critique_continuation_prompt, critique_prompt
from typing import Dict, List


def critique_draft_story(
    draft_text: str, sketch: str, model_used: str = "llama3"
) -> str:
    llm = get_ollama(model=model_used, temperature=0.7, top_k=30, verbose=False)
    prompt = critique_prompt()
    chain = prompt | llm | StrOutputParser()
    critique = chain.invoke({"story": draft_text, "sketch": sketch})
    return critique.strip()


def critique_draft_for_continuation(
    draft_text: str, context: str, model: str = "llama3"
) -> str:
    llm = get_ollama(model=model, temperature=0.7, top_k=30, verbose=False)
    prompt = critique_continuation_prompt()
    chain = prompt | llm | StrOutputParser()
    critique = chain.invoke({"draft": draft_text, "context": context})
    return critique.strip()
