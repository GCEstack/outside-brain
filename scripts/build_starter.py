import argparse
from datetime import datetime
from pathlib import Path

from scripts.config import load_project_domain_map
from scripts.domain_reader import read_domain_pack
from scripts.profile_reader import read_profile_section
from scripts.project_parser import parse_project_profile


def build_starter(project_root: Path, project_name: str) -> Path:
    mapping = load_project_domain_map(project_root)
    domains = mapping.get(project_name, [])

    lares_profile_root = project_root.parent / "lares-profile"
    scraper_root = project_root.parent / "ACTIVE" / "kimi-chat-scraper"

    persona = read_profile_section(lares_profile_root, "lares-profile", "Persona")
    voice = read_profile_section(lares_profile_root, "lares-voice", "Voice")
    memory = read_profile_section(lares_profile_root, "lares-memory", "Memory")

    project_profile_path = scraper_root / "profiles" / f"{project_name}.md"
    project_info = parse_project_profile(project_profile_path)

    twin_profile = read_profile_section(project_root, "outside-brain-profile", "Profile")

    lines = [
        f"# Chat Starter: {project_name}",
        f"Generated: {datetime.utcnow().isoformat()}Z",
        "",
        "## Lares Persona & Voice",
        "",
        persona,
        "",
        voice,
        "",
        memory,
        "",
        "## outside-brain Twin Note",
        "",
        twin_profile,
        "",
        "## What We've Done Well",
        "",
        f"Conversations in archive: {project_info['conversations']}",
        "",
        project_info["summary"],
        "",
        "## What the Archive Contains",
        "",
    ]

    for domain in domains:
        domain_path = lares_profile_root / "extracted" / "by-domain" / f"{domain}.md"
        pack = read_domain_pack(domain_path)
        lines.append(f"### {domain}")
        lines.append(f"- Threads: {pack['count']}")
        lines.append(f"- Route: {pack['route']}")
        lines.append(f"- Apps: {', '.join(pack['sources'])}")
        lines.append("")
        lines.append("**Snippets:**")
        for snippet in pack["snippets"][:5]:
            lines.append(f"- {snippet}")
        lines.append("")

    lines.extend([
        "## Goal for This Chat",
        "",
        "_Fill in before pasting._",
        "",
        "## Instructions for the AI",
        "",
        "- Stay on the project topic above.",
        "- Defer to Osito and Lares when context is unclear.",
        "- Do not invent facts not present in the provided context.",
        "",
    ])

    output_path = (
        project_root
        / "starters"
        / "pending-review"
        / f"{project_name} - {datetime.utcnow().strftime('%Y%m%d')}.md"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Build a reviewable chat starter")
    parser.add_argument("--project", help="Project name (e.g. 'EC8 Edge Crew')")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    mapping = load_project_domain_map(project_root)

    project_name = args.project
    if not project_name:
        print("Available projects:")
        for name in sorted(mapping):
            print(f"  - {name}")
        project_name = input("\nProject name: ").strip()

    if project_name not in mapping:
        print(f"Unknown project: {project_name}")
        raise SystemExit(1)

    output_path = build_starter(project_root, project_name)
    print(f"Starter written to: {output_path}")


if __name__ == "__main__":
    main()
