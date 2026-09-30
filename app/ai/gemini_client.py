from functools import lru_cache

from google import genai

from ..config import get_settings


@lru_cache
def get_client():
    settings = get_settings()

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_text(prompt: str, model: str) -> str:
    client = get_client()

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()