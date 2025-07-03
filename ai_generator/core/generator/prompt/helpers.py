from langchain_core.prompts import PromptTemplate


def event_extraction_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["content"],
        template="""
You are an expert story event analyst.

Your task is to extract and list **key story events** from the following story text.

---

Content to analyze:
{content}

---

**INSTRUCTIONS:**
- Break the text into 2-5 significant events that drive the story.
- For each event, extract:

  - event_type: One of [plot_point, character_development, conflict_escalation, resolution, discovery]
  - event_description: A short, clear sentence describing what happened.
  - characters_involved: List of character names involved.
  - emotional_impact: One of [high, medium, low]
  - consequences: List 1-3 consequences or outcomes.
  - setup_for_future: Boolean indicating if this event foreshadows or sets up future conflict.

---

**OUTPUT REQUIREMENTS:**
- Return a JSON array with one object per event.
- Each object must follow this JSON structure exactly:

{{
  "event_type": "string",
  "event_description": "string",
  "characters_involved": ["string", "string"],
  "emotional_impact": "string",
  "consequences": ["string", "string"],
  "setup_for_future": true
}}

---

**EXAMPLE OUTPUT:**

[
  {{
    "event_type": "conflict_escalation",
    "event_description": "Alice argues with Bob about the missing map.",
    "characters_involved": ["Alice", "Bob"],
    "emotional_impact": "high",
    "consequences": ["Trust is broken", "They split up"],
    "setup_for_future": true
  }},
  ...
]

---

ONLY output valid JSON with no commentary. Return only the JSON object.
""",
    )


def metadata_extraction_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["story"],
        template="""
You are an expert story analyst.

Given the following sketchboard and story text, extract key metadata in JSON format.

---
**Sketch**
\"\"\"
{sketch}
\"\"\"
---

**Story:**
\"\"\"
{story}
\"\"\"

---

**Output JSON Format:**

{{
  "current_status: "...",
  "main_theme": "...",
  "central_conflict": "...",
  "target_age_group": "...",
  "emotional_arc": "...",
  "story_summary": "...",
  "last_emotional_state": "...",
  "next_planned_direction": "..."
}}

---

Return only valid JSON with no extra commentary. Only json as output.
""",
    )


def image_generation_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["sketch","story"],
        template="""
Create a detailed image generation prompt in around 100 words for a professional book cover based on the provided sketch and story elements.

SKETCH ELEMENTS:
{sketch}

STORY CONTEXT:
{story}

Generate a comprehensive image prompt that includes:

VISUAL COMPOSITION:
- Incorporate visual elements that can be in the cover of this book.
- Design for book cover proportions
- Create compelling focal points and visual hierarchy

SETTING & CHARACTER PRIORITIES:
- Prioritize the most visually striking elements from the sketch.
- You can keep it abstract, like flowers, colorful, pale, dark, bright, etc.
- If the location/setting is magnificent or unique, you should ask to make it the main point of the cover.
- Characters are optional. The cover should be visually fantastic.
- Include architectural, landscape, or environmental details that create wow factor, if present.
- Maintain authentic period/genre styling if specified

MOOD & ATMOSPHERE:
- Match the emotional tone of the story.
- Use appropriate lighting, color palette, and weather conditions
- Create genre-appropriate atmosphere.

TECHNICAL SPECIFICATIONS:
- High resolution, professional book cover quality
- No text in the image.
- Balanced composition that works at thumbnail size
- Avoid cluttered or busy backgrounds behind potential text areas.

OUTPUT FORMAT:
Provide a single, detailed paragraph describing the complete book cover image. Be specific about colors, lighting, element positioning, background elements, and overall composition. Include all elements naturally integrated into a cohesive, marketable book cover design.

FINAL IMAGE PROMPT:
""",
    )
