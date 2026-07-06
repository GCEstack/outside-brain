from pathlib import Path


def read_profile_section(project_root: Path, profile_name: str, section_name: str) -> str:
    profile_path = project_root / "profile" / f"{profile_name}.md"
    text = profile_path.read_text(encoding="utf-8")
    marker = f"## {section_name}"
    if marker not in text:
        return ""
    start = text.index(marker) + len(marker)
    end = text.find("\n## ", start)
    if end == -1:
        end = len(text)
    return text[start:end].strip()
