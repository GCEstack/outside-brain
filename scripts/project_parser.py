from pathlib import Path


def parse_project_profile(profile_path: Path) -> dict[str, str | list[str]]:
    text = profile_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = lines[0].replace("# Profile:", "").strip() if lines else "Unknown"
    conversations = "0"
    for line in lines:
        if line.lower().startswith("conversations:"):
            conversations = line.split(":", 1)[1].strip()
            break
    summary = ""
    in_summary = False
    for line in lines:
        if line.strip() == "## Summary":
            in_summary = True
            continue
        if in_summary and line.startswith("## "):
            break
        if in_summary:
            summary += line + "\n"
    return {
        "title": title,
        "conversations": conversations,
        "summary": summary.strip(),
    }
