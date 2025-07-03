from core.generator.llm.ollama_llm import get_ollama
from langchain_core.output_parsers import JsonOutputParser

from core.generator.prompt.helpers import metadata_extraction_prompt


def extract_story_metadata(
    sketch: str, story_text: str, model_name: str = "mistral"
) -> dict:
    llm = get_ollama(model=model_name, temperature=0.2, top_p=1, verbose=False)
    prompt = metadata_extraction_prompt()
    chain = prompt | llm | JsonOutputParser()

    return chain.invoke({"story": story_text, "sketch": sketch})
