from core.generator.llm.ollama_llm import get_ollama
from core.generator.prompt.title import title_prompt
from langchain_core.output_parsers import StrOutputParser


def generate_title(story: str, model_name: str = "llama3") -> str:
    llm = get_ollama(
        model=model_name, temperature=2.0, verbose=False, top_k=40, top_p=1.1
    )
    prompt = title_prompt()
    chain = prompt | llm | StrOutputParser()
    title = chain.invoke({"story": story})
    return title.strip()
