from pathlib import Path


def read_domain_pack(domain_md_path: Path) -> dict[str, str | list[str]]:
    text = domain_md_path.read_text(encoding="utf-8")
    count = "0"
    route = ""
    sources = []
    snippets = []
    for line in text.splitlines():
        if line.startswith("- **Thread count:**"):
            count = line.split(":**")[1].strip()
        elif line.startswith("- **Route:**"):
            route = line.split(":**")[1].strip()
        elif line.startswith("- Apps:"):
            sources = [s.strip() for s in line.replace("- Apps:", "").split(",")]
        elif line.startswith("- `"):
            snippet = line.split(": ", 1)[1].strip().rstrip(".")
            snippets.append(snippet)
    return {
        "count": count,
        "route": route,
        "sources": sources,
        "snippets": snippets,
    }
