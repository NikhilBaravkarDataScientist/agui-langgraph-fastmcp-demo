import os
from langchain_openai import ChatOpenAI

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError(
                "OPENAI_API_KEY is not set. "
                "LLM cannot be initialized."
            )
        _llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )
    return _llm
