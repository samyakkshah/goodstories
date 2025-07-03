from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from core.generator.llm.ollama_llm import get_ollama
from core.generator.prompt.continuation import continuation_prompt


def generate_next_page_text(
    recap: str,
    tone: str,
    genre: str,
    current_status: str,
    character_context: str,
    model: str = "gemma3",
) -> str:
    prompt = continuation_prompt()

    llm = get_ollama(model=model)
    chain = prompt | llm | StrOutputParser()

    result = chain.invoke(
        {
            "recap": recap,
            "tone": tone,
            "genre": genre,
            "current_status": current_status,
            "character_context": character_context,
        }
    )

    return result.strip()
