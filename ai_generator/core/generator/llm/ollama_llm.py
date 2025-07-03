from typing import Literal, Optional, Union
from langchain_ollama import OllamaLLM


# 💡 This can be extended later with model registry, streaming, etc.
def get_ollama(
    temperature: float = 0.8,
    top_k: int = 40,
    top_p: float = 0.9,
    verbose: bool = False,
    format: Literal["", "json"] = "",
    num_ctx: Optional[int] = None,
    keep_alive: Optional[Union[int, str]] = None,
    model: str = "llama3",
) -> OllamaLLM:
    return OllamaLLM(
        model=model,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        verbose=verbose,
        format=format,
        num_ctx=num_ctx,
        keep_alive=keep_alive,
    )
