import os
from typing import Any

try:
    from google import genai
except ImportError:
    genai = None


def _get_prompt_text(prompt: Any) -> str:
    """Convert PromptRequest, dict, or string into plain prompt text."""

    if isinstance(prompt, str):
        return prompt.strip()

    # Pydantic request model
    if hasattr(prompt, "prompt"):
        value = getattr(prompt, "prompt", "")
        return str(value).strip() if value is not None else ""

    # Dictionary request
    if isinstance(prompt, dict):
        value = prompt.get("prompt", "")
        return str(value).strip()

    return str(prompt).strip()


def generate_outline(prompt: Any, **kwargs: Any) -> str:
    """Generate a comic outline using Gemini or a local fallback."""

    prompt_text = _get_prompt_text(prompt)

    if not prompt_text:
        prompt_text = "Create an exciting comic adventure."

    api_key = os.getenv("GEMINI_API_KEY")

    # Use local fallback if Gemini is not configured.
    if genai is None or not api_key:
        return _fallback_outline(prompt_text)

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=(
                "Create a short comic outline from this idea. "
                "Include a beginning, middle, and ending.\n\n"
                f"Comic idea: {prompt_text}"
            ),
        )

        text = getattr(response, "text", None)

        if text:
            return text

    except Exception as exc:
        print(f"Gemini Flash error: {exc}")

    # Always fall back instead of crashing.
    return _fallback_outline(prompt_text)


def _fallback_outline(prompt: Any) -> str:
    """Generate a local outline without requiring an AI API."""

    prompt_text = _get_prompt_text(prompt)

    if not prompt_text:
        prompt_text = "Untitled Adventure"

    title = prompt_text[:60]

    return (
        f"Comic Title: {title}\n\n"
        "Act 1 — Setup:\n"
        "Introduce the main character and the central situation.\n\n"
        "Act 2 — Conflict:\n"
        "The character encounters an unexpected challenge.\n\n"
        "Act 3 — Resolution:\n"
        "The character solves the problem and reaches a satisfying ending."
    )


__all__ = ["generate_outline"]
