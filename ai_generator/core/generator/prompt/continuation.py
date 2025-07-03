from langchain_core.prompts import PromptTemplate


def continuation_prompt() -> PromptTemplate:
    prompt = PromptTemplate(
        input_variables=[
            "recap",
            "character_context",
            "genre",
            "tone",
            "current_status",
        ],
        template="""
        Previously on the story:
{recap}

Main Characters:
{character_context}

Story tone: {tone}
Genre: {genre}
Current situation: {current_status}

- Continue the story in the same emotional tone and narrative style. Keep the pacing natural, and stay grounded in the character’s journey.
- Write in 250-500 words

Write the next page:

Only give me the **next page** of this **story**, as plain text. Don't add explanation or anything other than the story.
""",
    )
    return prompt
