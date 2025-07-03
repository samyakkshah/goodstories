from langchain_core.prompts import PromptTemplate


def title_prompt() -> PromptTemplate:
    prompt = PromptTemplate(
        input_variables=["story"],
        template="""
You are an excellent book title writer.

I'll give you a story, and you have to give me a good engaging title for it that is very indulging to read the story, and it should not be generic.

Content:
{story}

Only give me the **title** as plain text. No other explanation outside of it.
""",
    )
    return prompt
