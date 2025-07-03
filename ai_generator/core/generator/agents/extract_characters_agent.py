from core.generator.llm.ollama_llm import get_ollama
from core.generator.prompt.extract_characters import (
    extract_character_prompt,
    extract_new_character_prompt,
)
from langchain_core.output_parsers import JsonOutputParser


def extract_character_data(sketch: str, model_name: str = "mistral"):
    llm = get_ollama(
        model=model_name, temperature=0.1, top_p=3, format="json", verbose=False
    )
    prompt = extract_character_prompt()
    try:
        chain = prompt | llm | JsonOutputParser()
        char_data = chain.invoke({"sketch": sketch})
    except:
        char_data = {}
        print("Error in extraction")
    return char_data


def extract_new_character_data(sketch: str, model_name: str = "mistral"):
    llm = get_ollama(
        model=model_name, temperature=0.3, top_p=3, format="json", verbose=False
    )
    prompt = extract_new_character_prompt()
    try:
        chain = prompt | llm | JsonOutputParser()
        char_data = chain.invoke({"sketch": sketch})
    except:
        char_data = {"new_characters": []}
        print("Error in extraction")
    print(char_data)
    return char_data["new_characters"]
