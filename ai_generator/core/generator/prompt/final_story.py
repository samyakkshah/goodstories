from langchain_core.prompts import PromptTemplate


def final_story_prompt() -> PromptTemplate:
    prompt = PromptTemplate(
        input_variables=["title", "sketch", "draft", "critique"],
        template="""
You are a master storyteller at the peak of your craft, with the ability to transform rough material into literary gold.

You have been given a story idea, an initial draft, and professional editorial feedback. Your task is to synthesize all three into a polished, emotionally powerful final story that readers will remember long after finishing.

---

Original Story Idea:
\"\"\"
{sketch}
\"\"\"

---

Initial Draft:
\"\"\"
{draft}
\"\"\"

---

Editorial Analysis:
\"\"\"
{critique}
\"\"\"

---

Create the final version of this story (300-500 words) by:

• Implementing the strongest suggestions from the critique
• Don't change what is already working in the draft.
• Preserving the core emotional truth of the original concept
• Enhancing sensory details and cinematic moments
• Strengthening character voice and motivation
• Improving pacing and emotional rhythm
• Crafting a more impactful ending that satisfies yet opens possibilities
• Ensuring every sentence serves the story's emotional core.

--

**Very important**
- The draft is only to be refined.
- You don't omit things from the draft. Everything in the draft needs to be in the final version.
- Don't always start with 'As ...'
- You just have to understand the critical points and write what is not working or missing.

Write with the precision of a poet, the pacing of a filmmaker, and the emotional intelligence of a master psychologist. Create something that feels both inevitable and surprising.

---

Output Requirements:
- Deliver only the refined story text.
- No commentary, no title, no explanations
- Just the final story itself, polished to perfection. 
- Don't even tell me "Here is the refined version" or "here is the polished text".

---

Only return the final story. Don't add title in your response.
""",
    )
    return prompt


def final_continuation_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["context", "draft", "critique", "character_context"],
        template="""


You are an elite story architect, wielding narrative mastery to transform raw material into unforgettable fiction.


CHARACTERS IN PLAY:
{character_context}


---

STORY DRAFT:
{draft}

EDITORIAL GUIDANCE:
{critique}

----

Create the final version of this story (300-500 words) by:

• Implementing the strongest suggestions from the critique
• Don't change what is already working in the draft.
• Preserving the core emotional truth of the original concept
• Enhancing sensory details and cinematic moments
• Strengthening character voice and motivation
• Improving pacing and emotional rhythm
• Crafting a more impactful ending that satisfies yet opens possibilities
• Ensuring every sentence serves the story's emotional core.


---

**Very important**
- The draft is to be refined by changing what the critiques says.
- You don't omit things from the draft.
- Don't always start with 'As ...'
- You just have to understand the critical points and write what is not working or missing.

---

Output Requirements:
- Deliver only the refined story text.
- No commentary, no title, no explanations
- Just the final story itself, polished to perfection. 
- Don't even tell me "Here is the refined version" or "here is the polished text".

---

Only return the final story. Don't add title in your response.
- Don't ask me anything after ending.
""",
    )
