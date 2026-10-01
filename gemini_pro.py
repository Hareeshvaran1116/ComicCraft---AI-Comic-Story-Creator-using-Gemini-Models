import os
from typing import Any

try:
    from google import genai
except ImportError:
    genai = None


def generate_story(prompt: str, **kwargs: Any) -> str:
    """
    Generate a comic story using Gemini when configured.

    If Gemini is unavailable, return a local fallback so that
    ComicCraft can still be tested without an API key.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if genai is None or not api_key:
        return _fallback_story(prompt)

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=(
                "Write a creative comic story based on this idea. "
                "Keep it suitable for a general audience and divide "
                "the story into clear scenes.\n\n"
                f"Comic idea: {prompt}"
            ),
        )

        text = getattr(response, "text", None)

        if text:
            return text

        return _fallback_story(prompt)

    except Exception:
        return _fallback_story(prompt)


def _fallback_story(prompt: str) -> str:
    title = prompt[:60] if prompt else "The Unexpected Adventure"

    return (
        f"Title: {title}\n\n"
        "Scene 1 — The Beginning\n"
        "Our hero discovers that something unusual is happening.\n\n"
        "Scene 2 — The Challenge\n"
        "A surprising problem appears, forcing the hero to take action.\n\n"
        "Scene 3 — The Adventure\n"
        "The hero follows the clues and discovers an unexpected solution.\n\n"
        "Scene 4 — The Ending\n"
        "The problem is resolved, and the hero learns something valuable."
    )


__all__ = ["generate_story"]