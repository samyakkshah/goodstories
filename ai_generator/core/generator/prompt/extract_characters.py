from langchain_core.prompts import PromptTemplate


def extract_character_prompt() -> PromptTemplate:
    prompt = PromptTemplate(
        input_variables=["sketch"],
        template="""
You are a character analysis expert. Extract and structure all character information from the provided story sketchboard with precision and completeness.

---

Story Sketchboard:
{sketch}

---

Parse the character details and return a well-structured JSON object. For any missing information, make reasonable inferences based on the story context, genre, and tone.

Required JSON Structure:

{{
  "main_characters": [
  {{
    "name": "string",
      "age": "integer",
      "role": "string",
      "core_desire": "string",
      "deepest_fear": "string",
      "current_situation": "string",
      "personality_traits": ["string", "string"],
      "current_emotional_state": "string",
      "character_arc_stage": "string",
      "last_action": "string",
      "motivation_evolution": "string",
  }},
  ],


  "secondary_characters": [
    {{
      "name": "string (extract or create if unnamed)",
      "age": "integer (estimate if not specified)",
      "role": "string (their function/occupation)",
      "core_desire": "string",
      "deepest_fear": "string",
      "current_situation": "string",
      "personality_traits": ["string", "string"],
      "current_emotional_state": "string",
      "character_arc_stage": "string",
      "last_action": "string",
      "motivation_evolution": "string"z
      "relationship_to_main": "string (ally, enemy, love interest, etc.)",
      "description": "string (key characteristics or background)",
      "significance": "string (why they matter to the story)"
    }}
  ],
  "relationships": [
        {{
          "character_1_name": "string",
          "character_2_name": "string",
          "relationship_type": "string (ally, enemy, love interest, family, mentor)"
        }},
        ...
      ]
}}

Guidelines:
- Only give names from context. Do not add your own.
- Ages should be realistic estimates based on roles and context
- Personality traits should be 2-4 key descriptors
- Include all mentioned characters, even if briefly described
- Make logical inferences to fill gaps while staying true to the source material.

Return only valid JSON. No explanations, comments, or additional text.
""",
    )
    return prompt


def extract_new_character_prompt() -> PromptTemplate:
    prompt = PromptTemplate(
        input_variables=["sketch"],
        template="""
Extract character information from this story sketchboard and return valid JSON.
---

SKETCHBOARD:
{sketch}

---
EXTRACTION RULES:
- Only extract characters explicitly mentioned in the text
- Use exact names from the sketchboard - do not create new names
- If no name is given, use their role (e.g., "teacher", "neighbor")
- Only fill fields with information actually present in the text
- For missing information, use null or empty string
- Separate characters into the correct categories as labeled in the sketchboard

JSON FORMAT:
{{
  "main_characters": [
    {{
      "name": "string",
        "age": "integer",
        "role": "string",
        "core_desire": "string",
        "deepest_fear": "string",
        "current_situation": "string",
        "personality_traits": ["string", "string"],
        "current_emotional_state": "string",
        "character_arc_stage": "string",
        "last_action": "string",
        "motivation_evolution": "string",
    }},
    ...
  ],


  "secondary_characters": [
    {{
      "name": "string (extract or create if unnamed)",
      "age": "integer (estimate if not specified)",
      "role": "string (their function/occupation)",
      "core_desire": "string",
      "deepest_fear": "string",
      "current_situation": "string",
      "personality_traits": ["string", "string"],
      "current_emotional_state": "string",
      "character_arc_stage": "string",
      "last_action": "string",
      "motivation_evolution": "string"z
      "relationship_to_main": "string (connection described in the text. For example: ally, enemy, love interest, etc.)",
      "description": "string (key characteristics or background)",
      "significance": "string (why they matter to the story)"
    }},
    ...
  ],
  
  "new_characters": [
    {{
      "name": "string (extract or create if unnamed)",
      "age": "integer (estimate if not specified)",
      "role": "string (their function/occupation)",
      "core_desire": "string",
      "deepest_fear": "string",
      "current_situation": "string",
      "personality_traits": ["string", "string"],
      "current_emotional_state": "string",
      "character_arc_stage": "string",
      "last_action": "string",
      "motivation_evolution": "string"z
      "relationship_to_main": "string (connection described in the text. For example: ally, enemy, love interest, etc.)",
      "description": "string (key characteristics or background)",
      "significance": "string (why they matter to the story)"
    }}
  ]
}}

IMPORTANT:
- Look for section headers like "Current Characters","Main Characters", "Secondary Characters:", "New Characters:"
- Only include characters listed under "New Characters" in the new_characters array
- Use exact text from sketchboard - do not infer or add details not present
- Return valid JSON only, no other text
""",
    )
    return prompt
