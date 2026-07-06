import json
from pathlib import Path


def read_chat(chat_json_path: Path) -> dict[str, str | list[dict]]:
    with chat_json_path.open(encoding="utf-8") as f:
        return json.load(f)


def extract_user_messages(chat: dict) -> list[str]:
    return [
        m["content"]
        for m in chat.get("messages", [])
        if m.get("role") == "user" and isinstance(m.get("content"), str)
    ]
