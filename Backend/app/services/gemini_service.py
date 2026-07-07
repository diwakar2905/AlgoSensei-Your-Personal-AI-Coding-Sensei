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


import random

FREE_MODELS = ["gemini-1.5-flash", "gemini-2.5-flash", "gemini-1.5-pro"]


@lru_cache(maxsize=10)
def get_llm_for_model(model_name: str) -> ChatGoogleGenerativeAI:
    settings = get_settings()
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=settings.google_api_key,
        temperature=settings.temperature,
    )


def get_model_pipeline() -> list[str]:
    # Prioritize any model specified in environment variables or settings
    primary = os.getenv("GEMINI_MODEL")
    settings_model = get_settings().gemini_model
    
    models = []
    if primary:
        models.append(primary)
    elif settings_model:
        models.append(settings_model)
        
    # Append other free models, making sure we don't duplicate
    for m in FREE_MODELS:
        if m not in models:
            models.append(m)
            
    # Shuffle the fallback models to distribute request load and avoid rate limits
    if len(models) > 1:
        fallbacks = models[1:]
        random.shuffle(fallbacks)
        models = [models[0]] + fallbacks
        
    return models


def run_text_prompt(prompt_template, variables: dict[str, Any]) -> str:
    models = get_model_pipeline()
    last_error = None
    
    for model_name in models:
        try:
            llm = get_llm_for_model(model_name)
            chain = prompt_template | llm | StrOutputParser()
            return chain.invoke(variables)
        except Exception as e:
            print(f"Model '{model_name}' failed: {e}. Trying fallback...")
            last_error = e
            continue
            
    # If all models fail, raise the last exception
    if last_error:
        raise last_error
    raise Exception("No Gemini models available.")


def run_json_prompt(prompt_template, variables: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
    raw_text = run_text_prompt(prompt_template, variables)
    return safe_json_parse(raw_text, fallback)

