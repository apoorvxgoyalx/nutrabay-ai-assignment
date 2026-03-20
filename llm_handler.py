

"""
llm_handler.py
--------------
Handles all interactions with the Groq LLM API.
Includes prompt engineering and structured JSON output parsing.
"""
 
import os
import json
import re
from typing import Optional
 
 
# ── Prompt template ───────────────────────────────────────────────────────────
 
SYSTEM_PROMPT = """You are an expert instructional designer and corporate trainer.
Your task is to analyze Standard Operating Procedure (SOP) documents and convert them
into comprehensive, structured training modules for employees.
 
You MUST respond with ONLY valid JSON — no markdown fences, no prose, no extra text.
The JSON must strictly follow the schema provided in each user message."""
 
 
def build_user_prompt(sop_text: str) -> str:
    """
    Build the user prompt that instructs the LLM to generate a training module.
 
    Args:
        sop_text: Cleaned SOP document text.
 
    Returns:
        Formatted prompt string.
    """
    # Sanitize unicode characters that Groq's API can't handle
    # Replace common smart punctuation with ASCII equivalents
    unicode_map = {
        '\u2013': '-',   # en-dash
        '\u2014': '--',  # em-dash
        '\u2018': "'",   # left single quote
        '\u2019': "'",   # right single quote
        '\u201c': '"',   # left double quote
        '\u201d': '"',   # right double quote
        '\u2022': '*',   # bullet
        '\u2026': '...',  # ellipsis
        '\u00a0': ' ',   # non-breaking space
    }
    for char, replacement in unicode_map.items():
        sop_text = sop_text.replace(char, replacement)
    # Catch-all: encode to ASCII, replacing anything still non-ASCII
    sop_text = sop_text.encode('ascii', errors='replace').decode('ascii')
 
    # Truncate very long SOPs to stay within token limits (~12k chars ≈ ~3k tokens)
    MAX_CHARS = 12_000
    if len(sop_text) > MAX_CHARS:
        sop_text = sop_text[:MAX_CHARS] + "\n\n[... document truncated for length ...]"
 
    return f"""Analyze the following SOP document and generate a complete training module.
 
SOP DOCUMENT:
\"\"\"
{sop_text}
\"\"\"
 
Generate a JSON object with EXACTLY this structure (no extra fields, no markdown):
 
{{
  "document_title": "string — inferred title of the SOP",
  "summary": {{
    "overview": "string — 2-3 sentence overview of what this SOP covers",
    "key_objectives": ["string", "string", ...],
    "important_rules": ["string", "string", ...]
  }},
  "training_steps": [
    {{
      "step_number": 1,
      "title": "string",
      "description": "string — clear explanation of this step",
      "example": "string — concrete real-world example or scenario",
      "tips": ["string", ...]
    }}
  ],
  "quiz": [
    {{
      "question_number": 1,
      "type": "mcq",
      "question": "string",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "answer": "A",
      "explanation": "string — why this is the correct answer"
    }},
    {{
      "question_number": 2,
      "type": "scenario",
      "question": "string — a realistic workplace scenario question",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "answer": "B",
      "explanation": "string"
    }}
  ]
}}
 
Rules:
- training_steps: Generate 4–8 logical steps covering the full SOP
- quiz: Generate exactly 5 questions — mix of 3 MCQs and 2 scenario-based
- All arrays must have at least 3 items unless the SOP is very short
- Be specific and practical — use actual content from the SOP
- Respond with ONLY the JSON object, nothing else
"""
 
 
# ── Groq API call ─────────────────────────────────────────────────────────────
 
def call_groq_llm(
    sop_text: str,
    api_key: Optional[str] = None,
    model: str = "llama3-70b-8192",
    temperature: float = 0.3,
) -> dict:
    """
    Send SOP text to Groq LLM and return parsed training module as a dict.
 
    Args:
        sop_text: Cleaned SOP document text.
        api_key: Groq API key. Falls back to GROQ_API_KEY env variable.
        model: Groq model identifier.
        temperature: Sampling temperature (lower = more deterministic).
 
    Returns:
        Parsed JSON dict containing summary, training_steps, and quiz.
 
    Raises:
        ValueError: If API key is missing or response JSON is malformed.
        RuntimeError: If the Groq API returns an error.
    """
    try:
        from groq import Groq
    except ImportError:
        raise ImportError("groq package not installed. Run: pip install groq")
 
    # Resolve API key
    resolved_key = api_key or os.environ.get("GROQ_API_KEY", "").strip()
    if not resolved_key:
        raise ValueError(
            "Groq API key not found. Set the GROQ_API_KEY environment variable "
            "or enter it in the sidebar."
        )
 
    client = Groq(api_key=resolved_key)
 
    user_prompt = build_user_prompt(sop_text)
 
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=4096,
        )
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "invalid_api_key" in error_msg.lower():
            raise RuntimeError("Invalid Groq API key. Please check your credentials.")
        elif "rate_limit" in error_msg.lower():
            raise RuntimeError(
                "Groq rate limit hit. Please wait a moment and try again."
            )
        else:
            raise RuntimeError(f"Groq API error: {error_msg}")
 
    raw_content = response.choices[0].message.content.strip()
 
    return parse_llm_response(raw_content)
 
 
def parse_llm_response(raw_content: str) -> dict:
    """
    Parse and validate the LLM's JSON response.
 
    Handles common LLM quirks like markdown code fences.
 
    Args:
        raw_content: Raw string response from the LLM.
 
    Returns:
        Validated dict.
 
    Raises:
        ValueError: If the response cannot be parsed as valid JSON.
    """
    # Strip markdown code fences if present
    cleaned = re.sub(r'^```(?:json)?\s*', '', raw_content, flags=re.MULTILINE)
    cleaned = re.sub(r'\s*```$', '', cleaned, flags=re.MULTILINE)
    cleaned = cleaned.strip()
 
    # Attempt JSON parse
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to extract JSON object from the response
        match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
            except json.JSONDecodeError:
                raise ValueError(
                    "The LLM returned malformed JSON. "
                    "Try again or simplify your SOP document."
                )
        else:
            raise ValueError(
                "Could not find a JSON object in the LLM response. "
                "Please try again."
            )
 
    # Basic schema validation
    required_keys = {"summary", "training_steps", "quiz"}
    missing = required_keys - set(data.keys())
    if missing:
        raise ValueError(
            f"LLM response is missing required fields: {', '.join(missing)}. "
            "Please try again."
        )
 
    return data

# ── Available models ──────────────────────────────────────────────────────────

AVAILABLE_MODELS = {
    "LLaMA 3 70B (Best Quality)": "llama-3.1-8b-instant",
    "LLaMA 3 8B (Faster)": "llama3-8b-8192",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 7B": "gemma-7b-it",
}
