from langchain_core.prompts import PromptTemplate


def story_prompt() -> PromptTemplate:
    prompt = PromptTemplate(
        input_variables=["genre", "tone"],
        template="""
        You are a brilliant storyteller known for writing emotionally powerful short stories
that feel like this can be a movie, or feels like a chapter from one of the best novels.

Write a complete short story in exactly one go. The story should:
- Be between 200 to 350 words
- Feel cinematic and immersive
- Have strong dopamine trigger to get readers hooked on.
- Be original (no clichés or tropes)
- End with a small twist or thought-provoking final line.
- This should be open ended to let this continue again.

**Genre**: {genre}

**Tone**: {tone}

Start with a strong opening sentence. Write in natural, beautiful prose. Do not use bullet points or headings.
Return only the **story** as plain text as ouput. No other explanation
""",
    )
    return prompt


def continuation_prompt() -> PromptTemplate:
    prompt = PromptTemplate(
        input_variables=["past_chapters", "page_number", "genre", "tone"],
        template="""
        
        You previously wrote this story:

"{past_chapters}"

Now continue the story meaningfully. This is page {page_number}.
Maintain tone and style. Preserve character and emotional arc.
Add depth but keep it concise.

Genre: {genre}
Tone: {tone}

Return only the **story** as plain text as ouput. No other explanation 
""",
    )
    return prompt
