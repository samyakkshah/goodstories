from core.generator.llm.ollama_llm import get_ollama
from core.generator.prompt.helpers import image_generation_prompt
from langchain_core.output_parsers import StrOutputParser


def generate_image_prompt(sketch:str, story: str, model_name: str = "llama3") -> str:
    llm = get_ollama(
        model=model_name, temperature=0.7,verbose=False, top_k=35, top_p=0.7
    )
    prompt = image_generation_prompt()
    chain = prompt | llm | StrOutputParser()
    title = chain.invoke({"sketch":sketch, "story": story})
    return title.strip()
