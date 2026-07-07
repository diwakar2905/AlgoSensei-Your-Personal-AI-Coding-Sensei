import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    google_api_key: str
    gemini_model: str = "gemini-1.5-flash"
    temperature: float = 0.4


def get_settings() -> Settings:
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found. Set it in Backend/python.env or your deployment environment.")

    return Settings(
        google_api_key=google_api_key,
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        temperature=float(os.getenv("GEMINI_TEMPERATURE", "0.4")),
    )
