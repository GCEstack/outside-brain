from pathlib import Path

from scripts.archive_reader import extract_user_messages, read_chat
from scripts.config import load_project_domain_map
from scripts.keyword_builder import build_keywords
from scripts.project_parser import parse_project_profile


def _find_chat_json_files(archive_root: Path) -> list[Path]:
    if not archive_root.exists():
        return []
    return sorted(archive_root.rglob("chat.json"))


def _score_conversation(chat_path: Path, keywords: set[str]) -> dict[str, str | int]:
    chat = read_chat(chat_path)
    user_messages = extract_user_messages(chat)
    user_text = " ".join(user_messages).lower()

    matched = {kw for kw in keywords if kw in user_text}
    total = len(keywords)
    score = int((len(matched) / total) * 100) if total else 0

    snippet = ""
    if user_messages:
        snippet = user_messages[0][:80]

    return {
        "title": chat.get("title", chat_path.parent.name),
        "date": chat.get("created_at", ""),
        "score": score,
        "snippet": snippet,
    }


def score_project_conversations(project_root: Path, project_name: str) -> list[dict[str, str | int]]:
    mapping = load_project_domain_map(project_root)
    domains = mapping.get(project_name, [])

    scraper_root = project_root.parent.parent / "ACTIVE" / "kimi-chat-scraper"
    project_profile_path = scraper_root / "profiles" / f"{project_name}.md"
    project_info = parse_project_profile(project_profile_path)

    keywords = build_keywords(project_name, project_info["summary"], domains)

    archive_root = scraper_root / "kimi-chat-archive"
    chat_files = _find_chat_json_files(archive_root)

    scored = [_score_conversation(p, keywords) for p in chat_files]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored
