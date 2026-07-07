import json
import os
import re
from functools import lru_cache
from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings


def format_history(history: list[Any]) -> str:
    lines: list[str] = []
    for message in history:
        role = getattr(message, "role", "user")
        parts = getattr(message, "parts", []) or []
        text = parts[0].get("text", "") if parts else ""
        lines.append(f"{role}: {text}")
    return "\n".join(lines)


def strip_markdown_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def safe_json_parse(text: str, fallback: dict[str, Any]) -> dict[str, Any]:
    try:
        return json.loads(strip_markdown_fences(text))
    except json.JSONDecodeError:
        return {**fallback, "raw_text": text}


@lru_cache(maxsize=1)
def get_llm() -> ChatGoogleGenerativeAI:
    settings = get_settings()
    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", settings.gemini_model),
        google_api_key=settings.google_api_key,
        temperature=settings.temperature,
    )


def run_text_prompt(prompt_template, variables: dict[str, Any]) -> str:
    chain = prompt_template | get_llm() | StrOutputParser()
    return chain.invoke(variables)


def run_json_prompt(prompt_template, variables: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
    raw_text = run_text_prompt(prompt_template, variables)
    return safe_json_parse(raw_text, fallback)
