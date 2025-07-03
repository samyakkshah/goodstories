from core.generator.llm.ollama_llm import get_ollama
from core.generator.prompt.helpers import event_extraction_prompt
from langchain_core.output_parsers import JsonOutputParser


def extract_story_events_from_text(content: str, model_name: str = "mistral") -> list:
    llm = get_ollama(model=model_name, temperature=0.2, top_p=0.7, verbose=False)
    prompt = event_extraction_prompt()
    chain = prompt | llm | JsonOutputParser()

    events = chain.invoke({"content": content})
    return events
