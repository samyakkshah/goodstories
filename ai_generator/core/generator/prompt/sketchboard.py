from langchain_core.prompts import PromptTemplate


def sketchboard_prompt() -> PromptTemplate:
    prompt = PromptTemplate(
        input_variables=["genre", "tone", "names"],
        template="""
You are a well experienced and master at story writing.

Create a story sketchboard using the following specifications:

Genre: {genre}
Tone: {tone}

Character Data (to help you select. These are just for help. Optional): 
\"\"\"
{names} 
\"\"\"

---

REQUIRED OUTPUT FORMAT - Fill each section completely:

**Genre:** [Specify the genre]

**Tone:** [Specify the tone]

**Main Character(s):**
- Name, age, basic appearance
- What they want most
- What they fear most
- Current situation

**Secondary Characters (2-3):**
- Name, age, basic appearance
- relationship to main character
- Key trait or role in story
- What they want most
- What they fear most
- Current situation

**Setting:**
- Location and time
- Why the main character is there

**Story Outline:**
1. Opening hook (1 sentence)
2. Initial conflict/problem
3. Character's first attempt to solve it
4. Plot (3-4 sentences)
5. Complication or setback
6. Character's realization or change
7. Resolution

**Theme:** What is this story really about? (1-2 sentences)

**Target Age Group:** What age should the story be made for?

---

INSTRUCTIONS:
- Write clearly and concisely
- Focus on one central conflict
- Make the main character's goal specific and relatable
- Ensure each story beat connects logically to the next
- Output ONLY the filled template above
""",
    )
    return prompt


def sketchboard_prompt_for_continuation() -> PromptTemplate:
    prompt = PromptTemplate(
        input_variables=[
            "genre",
            "tone",
            "context",
            "character_context",
            "names",
        ],
        template="""
You are a master story architect with a cinematic imagination and a deep understanding of emotional storytelling, narrative structure, and character psychology.

Use the following comprehensive context to plan the next page of the story. 
Maintain continuity in location, conflicts, mood, character emotional states, arcs, and relationships. 
Introduce new tensions or events that evolve the story naturally.

---

PREVIOUS STORY CONTEXT:
\"\"\"
{context}
\"\"\"

---

STORY DETAILS:
Genre: {genre}
Tone: {tone}

CHARACTER CONTEXT:
\"\"\"
{character_context}
\"\"\"

Available Names: {names}

---

---

**REQUIRED OUTPUT FORMAT**
(Fill out EACH section fully and clearly. Do not skip or shorten.)

---
REQUIRED OUTPUT FORMAT - Fill each section:

**Genre:** [Same as input]

**Tone:** [Same as input]

**Current Characters:**
- Main: [Brief status update from where they left off]
- Secondary: [Their current situation]

**New Characters (if any):**
- Name, age, basic appearance
- relationship to main character
- Key trait or role in story
- What they want most
- What they fear most
- Current situation

**Setting:**
- Location (same or new)
- Time progression from previous scene

**Next Scene Outline:**
1. Opening: How does this scene connect to the previous ending?
2. New conflict or development
3. Character reactions/decisions
4. Complication or discovery
5. Character growth or change
6. Scene ending that sets up what comes next

**Character Goals:**
- What does each character want in this next scene?
- How have their goals changed from before?

---

INSTRUCTIONS:
- Build directly from the previous story's ending
- Advance the plot with new developments
- Keep characters consistent with their established personalities
- Create natural story progression
""",
    )
    return prompt
