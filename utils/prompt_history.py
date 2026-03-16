import json
from datetime import datetime
from pathlib import Path
from typing import Any


PROMPT_HISTORY_PATH = Path(__file__).resolve().parent.parent / "data" / "prompt_history.json"
MAX_HISTORY_ITEMS = 10


def _ensure_prompt_history_file() -> None:
    """Create the prompt history file with an empty list when it is missing."""
    PROMPT_HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not PROMPT_HISTORY_PATH.exists():
        PROMPT_HISTORY_PATH.write_text("[]", encoding="utf-8")


def load_prompt_history() -> list[dict[str, Any]]:
    """Return the recent prompt history from disk."""
    _ensure_prompt_history_file()

    try:
        history_data = json.loads(PROMPT_HISTORY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        history_data = []
        PROMPT_HISTORY_PATH.write_text("[]", encoding="utf-8")

    return history_data if isinstance(history_data, list) else []


def add_prompt_to_history(prompt_data: dict[str, Any]) -> None:
    """Add a newly generated prompt to recent history and keep only the latest items."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    task_type = str(prompt_data.get("task_type", "")).strip()
    subject = str(prompt_data.get("subject", "")).strip()
    grade = str(prompt_data.get("grade", "")).strip()

    label_parts = [part for part in [task_type or subject, grade] if part]
    label_prefix = " - ".join(label_parts) if label_parts else "Recent Prompt"
    entry = {
        "label": f"{label_prefix} - {timestamp}",
        "task_type": task_type,
        "subject": subject,
        "grade": grade,
        "difficulty": str(prompt_data.get("difficulty", "")).strip(),
        "question_type": str(prompt_data.get("question_type", "")).strip(),
        "prompt": str(prompt_data.get("prompt", "")).strip(),
        "created_at": timestamp,
    }

    history = load_prompt_history()
    history.insert(0, entry)
    trimmed_history = history[:MAX_HISTORY_ITEMS]
    PROMPT_HISTORY_PATH.write_text(json.dumps(trimmed_history, indent=2), encoding="utf-8")


def delete_history_prompt(label: str) -> bool:
    """Delete a history item by label. Returns True when removed."""
    history = load_prompt_history()
    updated_history = [item for item in history if item.get("label") != label]

    if len(updated_history) == len(history):
        return False

    PROMPT_HISTORY_PATH.write_text(json.dumps(updated_history, indent=2), encoding="utf-8")
    return True


def clear_prompt_history() -> None:
    """Remove all recent history items."""
    _ensure_prompt_history_file()
    PROMPT_HISTORY_PATH.write_text("[]", encoding="utf-8")


def get_history_prompts() -> list[str]:
    """Return prompt history labels for sidebar display."""
    return [item.get("label", "Recent Prompt") for item in load_prompt_history()]
