import json
from pathlib import Path
from typing import Any


PROMPT_LIBRARY_PATH = Path(__file__).resolve().parent.parent / "data" / "prompt_library.json"


def _ensure_prompt_library_file() -> None:
    """Create the prompt library file with an empty list when it is missing."""
    PROMPT_LIBRARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not PROMPT_LIBRARY_PATH.exists():
        PROMPT_LIBRARY_PATH.write_text("[]", encoding="utf-8")


def load_prompt_library() -> list[dict[str, Any]]:
    """Return the saved prompt library from disk."""
    _ensure_prompt_library_file()

    try:
        library_data = json.loads(PROMPT_LIBRARY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        library_data = []
        PROMPT_LIBRARY_PATH.write_text("[]", encoding="utf-8")

    return library_data if isinstance(library_data, list) else []


def save_prompt_to_library(prompt_data: dict[str, Any]) -> bool:
    """Save a prompt if its title is unique. Returns True when saved."""
    library = load_prompt_library()
    normalized_title = str(prompt_data.get("title", "")).strip()
    if not normalized_title:
        return False

    if any(item.get("title", "").strip().lower() == normalized_title.lower() for item in library):
        return False

    entry = {
        "title": normalized_title,
        "subject": str(prompt_data.get("subject", "")).strip(),
        "grade": str(prompt_data.get("grade", "")).strip(),
        "difficulty": str(prompt_data.get("difficulty", "")).strip(),
        "question_type": str(prompt_data.get("question_type", "")).strip(),
        "prompt": str(prompt_data.get("prompt", "")).strip(),
    }
    library.append(entry)
    PROMPT_LIBRARY_PATH.write_text(json.dumps(library, indent=2), encoding="utf-8")
    return True


def delete_prompt(title: str) -> bool:
    """Delete a saved prompt by title. Returns True when a prompt is removed."""
    normalized_title = title.strip().lower()
    library = load_prompt_library()
    updated_library = [item for item in library if item.get("title", "").strip().lower() != normalized_title]

    if len(updated_library) == len(library):
        return False

    PROMPT_LIBRARY_PATH.write_text(json.dumps(updated_library, indent=2), encoding="utf-8")
    return True


def get_prompt_list() -> list[str]:
    """Return saved prompt titles for sidebar display."""
    return [item.get("title", "Untitled Prompt") for item in load_prompt_library()]
