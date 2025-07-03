from langchain_core.prompts import PromptTemplate


def story_draft_prompt() -> PromptTemplate:
    prompt = PromptTemplate(
        input_variables=["sketch"],
        template="""

You are a master storyteller with the precision of Raymond Carver, the emotional depth of Alice Munro, and the cinematic vision of a film director.

Transform the following sketchboard into a complete, immersive story of 300-500 words.


---

Sketchboard:
\"\"\"
{sketch}
\"\"\"

---

WRITING REQUIREMENTS:
- Start with action or dialogue, not description
- Use the sketchboard's genre, tone, and age group
- Include all main characters from the sketchboard
- Follow the story outline provided
- Match the target age group's reading level

STYLE GUIDELINES:
- Show character emotions through actions and dialogue
- If it is a biography, write it in first personm as the main character is writing this story.
- Don't use phrases like "The air thickened" or too much description about "the air" around the characters. Avoid words like "shroud". Use more descriptive terms for saying what is happening.
- Use concrete, specific details
- Vary sentence lengths
- Include sensory details (what characters see, hear, feel)
- Make dialogue natural and brief
- Set this as a start of a bigger story.

FORMATTING:
- Put dialogue on separate lines with space above and below
- Use simple language for readers under 25
- Limit complex vocabulary to 3-5 words maximum

OUTPUT: Return only the story text. No title, explanations, or commentary.
""",
    )
    return prompt


def story_draft_prompt_for_continuation() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["context", "sketch", "rules"],
        template="""

You are a master storyteller with the emotional precision of Alice Munro, the narrative restraint of Raymond Carver, and the cinematic eye of a film director.
---

PREVIOUS SCENE (for context only - do NOT repeat or summarize):
\"\"\"
{context}
\"\"\"

---

Continue this above story by writing the next scene (300-500 words).


NEXT SCENE GUIDE:
\"\"\"
{sketch}
\"\"\"

---

STORY AND CHARACTER RULES YOU MUST FOLLOW:
{rules}

---

CONTINUATION REQUIREMENTS:
- Start immediately where the previous scene ended
- Use the same characters, tone, and setting established
- Follow the sketch's plot developments exactly
- Maintain the same writing style and voice
- Do NOT reintroduce characters already established
- Only introduce new characters if specified in the sketch

WRITING GUIDELINES:
- Continue the existing narrative flow seamlessly
- If it is a biography, write it in first personm as the main character is writing this story.
- Don't use phrases like "The air thickened" or too much description about "the air" around the characters. Avoid words like "shroud". Use more descriptive terms for saying what is happening.
- Keep dialogue natural and brief
- Use specific, concrete details
- Show character emotions through actions
- Match the established reading level
- End at a natural pause, not a conclusion

WHAT NOT TO DO:
- Do not repeat information from the previous scene
- Do not change the established tone or style
- Do not summarize what happened before
- Do not add characters not mentioned in the sketch
- Do not contradict previous events

OUTPUT: Write only the story continuation. No title, explanations, or commentary.
""",
    )
