# outside-brain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone external twin workspace that reads archived chat profiles and Lares domain packs, then generates reviewable project-scoped chat starters.

**Architecture:** Small Python scripts with single responsibilities: config loading, profile reading, project-profile parsing, domain-pack reading, and starter assembly. A CLI entry point composes these pieces and writes markdown to `starters/pending-review/`. Tests use temporary paths so they never touch real archives.

**Tech Stack:** Python 3.14, standard library only, pytest for tests.

## Global Constraints

- No modifications to `Projects/ACTIVE/kimi-chat-scraper/` or `Projects/PERSONAL/lares-profile/`.
- Read only the `.md` summaries from `extracted/by-domain/`, never the giant `.json` files.
- Every starter is a draft in `pending-review/` until Osito approves it.
- Standard library only; no external dependencies.
- All paths are relative to `Projects/PERSONAL/outside-brain/`.

---

### Task 1: Scaffold project structure

**Files:**
- Create: `README.md`
- Create: `profile/outside-brain-profile.md`
- Create: `profile/outside-brain-voice.md`
- Create: `profile/outside-brain-memory.md`
- Create: `config/project_domain_map.json`
- Create: `.gitignore`

**Interfaces:**
- Produces: the workspace skeleton and initial twin profile docs.

- [ ] **Step 1: Create README.md**

```markdown
# outside-brain

External twin to Lares. Reads archived chat history and generates reviewable chat starters.

## Quick Commands

```powershell
python scripts/build_starter.py --project "EC8 Edge Crew"
python scripts/build_starter.py
```

Starters are written to `starters/pending-review/`. Review before moving to `starters/ready-to-paste/`.
```

- [ ] **Step 2: Create twin profile docs**

`profile/outside-brain-profile.md`:

```markdown
# outside-brain — Profile

Twin to Lares. Operates outside the family system.
Role: read ported archives, understand project state, and draft chat starters for Osito's review.
```

`profile/outside-brain-voice.md`:

```markdown
# outside-brain — Voice

Concise, structured, observational. Does not replace Lares; complements her from the outside.
```

`profile/outside-brain-memory.md`:

```markdown
# outside-brain — Memory

- Mirrors Lares profile/voice docs.
- Tracks which archives have been read.
- Notes project states observed in the dumped chats.
```

- [ ] **Step 3: Create project-domain mapping config**

`config/project_domain_map.json`:

```json
{
  "EC8 Edge Crew": ["betting", "ec"],
  "Casa Companion": ["casa"],
  "Heartbeat Family System": ["personal"],
  "Kimi Code Ops": ["release-process", "uncategorized"],
  "AI Models & APIs": ["personal", "uncategorized"],
  "Voice & Audio": ["personal"],
  "Media & Video": ["personal"],
  "Creative & Brand": ["personal"],
  "Desktop & File Org": ["personal"]
}
```

- [ ] **Step 4: Create .gitignore**

```text
__pycache__/
.pytest_cache/
starters/pending-review/*
starters/ready-to-paste/*
!starters/pending-review/.gitkeep
!starters/ready-to-paste/.gitkeep
```

- [ ] **Step 5: Add .gitkeep files**

```bash
touch starters/pending-review/.gitkeep
touch starters/ready-to-paste/.gitkeep
```

- [ ] **Step 6: Commit**

```bash
git add README.md profile/ config/ .gitignore starters/
git commit -m "chore: scaffold outside-brain workspace"
```

---

### Task 2: Config loader

**Files:**
- Create: `scripts/config.py`
- Create: `tests/test_config.py`

**Interfaces:**
- Produces: `load_project_domain_map(project_root: Path) -> dict[str, list[str]]`

- [ ] **Step 1: Write the failing test**

`tests/test_config.py`:

```python
from pathlib import Path

from scripts.config import load_project_domain_map


def test_load_project_domain_map(tmp_path: Path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_path = config_dir / "project_domain_map.json"
    config_path.write_text('{"EC8 Edge Crew": ["betting", "ec"]}', encoding="utf-8")

    result = load_project_domain_map(tmp_path)

    assert result == {"EC8 Edge Crew": ["betting", "ec"]}
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m pytest tests/test_config.py -v
```

Expected: `ModuleNotFoundError: No module named 'scripts.config'`

- [ ] **Step 3: Write minimal implementation**

`scripts/config.py`:

```python
import json
from pathlib import Path


def load_project_domain_map(project_root: Path) -> dict[str, list[str]]:
    config_path = project_root / "config" / "project_domain_map.json"
    return json.loads(config_path.read_text(encoding="utf-8"))
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m pytest tests/test_config.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/config.py tests/test_config.py
git commit -m "feat: load project-to-domain mapping config"
```

---

### Task 3: Profile reader

**Files:**
- Create: `scripts/profile_reader.py`
- Create: `tests/test_profile_reader.py`

**Interfaces:**
- Produces: `read_profile_section(project_root: Path, profile_name: str, section_name: str) -> str`

- [ ] **Step 1: Write the failing test**

`tests/test_profile_reader.py`:

```python
from pathlib import Path

from scripts.profile_reader import read_profile_section


def test_read_profile_section(tmp_path: Path):
    profile_dir = tmp_path / "profile"
    profile_dir.mkdir()
    (profile_dir / "lares-profile.md").write_text(
        "# Lares Profile\n\n## Persona\nGuardian.\n", encoding="utf-8"
    )

    result = read_profile_section(tmp_path, "lares-profile", "Persona")

    assert "Guardian." in result
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m pytest tests/test_profile_reader.py -v
```

Expected: `ModuleNotFoundError` or `function not defined`

- [ ] **Step 3: Write minimal implementation**

`scripts/profile_reader.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m pytest tests/test_profile_reader.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/profile_reader.py tests/test_profile_reader.py
git commit -m "feat: read profile sections by heading"
```

---

### Task 4: Project profile parser

**Files:**
- Create: `scripts/project_parser.py`
- Create: `tests/test_project_parser.py`

**Interfaces:**
- Produces: `parse_project_profile(profile_path: Path) -> dict[str, str | list[str]]`

- [ ] **Step 1: Write the failing test**

`tests/test_project_parser.py`:

```python
from pathlib import Path

from scripts.project_parser import parse_project_profile


def test_parse_project_profile(tmp_path: Path):
    profile_path = tmp_path / "EC8 Edge Crew.md"
    profile_path.write_text(
        "# Profile: EC8 Edge Crew\r\n"
        "Generated: 2026-07-06\r\n"
        "Conversations: 5\r\n"
        "\r\n"
        "## Summary\r\n"
        "- **Edge** (account1, 10 messages)\r\n"
        "- **Take the shot** (account1, 5 messages)\r\n",
        encoding="utf-8",
    )

    result = parse_project_profile(profile_path)

    assert result["title"] == "EC8 Edge Crew"
    assert result["conversations"] == "5"
    assert "Edge" in result["summary"]
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m pytest tests/test_project_parser.py -v
```

Expected: `ModuleNotFoundError`

- [ ] **Step 3: Write minimal implementation**

`scripts/project_parser.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m pytest tests/test_project_parser.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/project_parser.py tests/test_project_parser.py
git commit -m "feat: parse kimi-chat-scraper project profile"
```

---

### Task 5: Domain pack reader

**Files:**
- Create: `scripts/domain_reader.py`
- Create: `tests/test_domain_reader.py`

**Interfaces:**
- Produces: `read_domain_pack(domain_md_path: Path) -> dict[str, str | list[str]]`

- [ ] **Step 1: Write the failing test**

`tests/test_domain_reader.py`:

```python
from pathlib import Path

from scripts.domain_reader import read_domain_pack


def test_read_domain_pack(tmp_path: Path):
    domain_path = tmp_path / "betting.md"
    domain_path.write_text(
        "# Lares — Betting Threads\n\n"
        "- **Thread count:** 744\n"
        "- **Route:** ec4-edge-crew-notes\n\n"
        "## Sources\n\n"
        "- Apps: claude, kimi\n\n"
        "## Thread snippets\n\n"
        "- `/a`: Edge crew odds...\n",
        encoding="utf-8",
    )

    result = read_domain_pack(domain_path)

    assert result["count"] == "744"
    assert result["route"] == "ec4-edge-crew-notes"
    assert "claude" in result["sources"]
    assert "Edge crew odds" in result["snippets"]
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m pytest tests/test_domain_reader.py -v
```

Expected: `ModuleNotFoundError`

- [ ] **Step 3: Write minimal implementation**

`scripts/domain_reader.py`:

```python
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
            snippets.append(line[2:].strip())
    return {
        "count": count,
        "route": route,
        "sources": sources,
        "snippets": snippets,
    }
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m pytest tests/test_domain_reader.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/domain_reader.py tests/test_domain_reader.py
git commit -m "feat: read Lares domain pack markdown summaries"
```

---

### Task 6: Starter builder and CLI

**Files:**
- Create: `scripts/build_starter.py`
- Create: `tests/test_build_starter.py`
- Create: `tests/fixtures/lares-profile/profile/lares-profile.md`
- Create: `tests/fixtures/kimi-chat-scraper/profiles/EC8 Edge Crew.md`
- Create: `tests/fixtures/lares-profile/extracted/by-domain/betting.md`

**Interfaces:**
- Consumes: `load_project_domain_map`, `read_profile_section`, `parse_project_profile`, `read_domain_pack`
- Produces: `build_starter(project_root: Path, project_name: str) -> Path`

- [ ] **Step 1: Write the failing test**

`tests/test_build_starter.py`:

```python
from pathlib import Path

from scripts.build_starter import build_starter


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_build_starter(tmp_path: Path):
    # Arrange: create a minimal twin workspace inside tmp_path
    _write(tmp_path / "config" / "project_domain_map.json", '{"EC8 Edge Crew": ["betting"]}')
    _write(
        tmp_path / "profile" / "outside-brain-profile.md",
        "# outside-brain Profile\n\nTwin.\n",
    )
    _write(
        tmp_path / "profile" / "lares-profile.md",
        "# Lares Profile\n\n## Persona\nGuardian.\n",
    )
    _write(
        tmp_path / "profile" / "lares-voice.md",
        "# Lares Voice\n\nDirect.\n",
    )
    _write(
        tmp_path / "profile" / "lares-memory.md",
        "# Lares Memory\n\nDomain packs linked.\n",
    )
    _write(
        tmp_path / ".." / "kimi-chat-scraper" / "profiles" / "EC8 Edge Crew.md",
        "# Profile: EC8 Edge Crew\r\nConversations: 5\r\n\r\n## Summary\r\n- **Edge** (account1, 10 messages)\r\n",
    )
    _write(
        tmp_path / ".." / "lares-profile" / "extracted" / "by-domain" / "betting.md",
        "# Lares — Betting Threads\n\n- **Thread count:** 744\n- **Route:** ec4-edge-crew-notes\n\n## Sources\n\n- Apps: claude, kimi\n\n## Thread snippets\n\n- `/a`: Edge crew odds...\n",
    )

    result = build_starter(tmp_path, "EC8 Edge Crew")

    assert result.exists()
    content = result.read_text(encoding="utf-8")
    assert "EC8 Edge Crew" in content
    assert "Guardian." in content
    assert "Edge crew odds" in content
    assert "pending-review" in str(result)
```

Note: This test uses `tmp_path / ".."` to place external fixture roots. Ensure the test uses absolute paths; `tmp_path` is absolute.

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m pytest tests/test_build_starter.py -v
```

Expected: `ModuleNotFoundError` for `scripts.build_starter`

- [ ] **Step 3: Write minimal implementation**

`scripts/build_starter.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m pytest tests/test_build_starter.py -v
```

Expected: PASS

- [ ] **Step 5: Run full test suite**

```bash
python -m pytest tests/ -v
```

Expected: all tests pass

- [ ] **Step 6: Commit**

```bash
git add scripts/build_starter.py tests/test_build_starter.py
git commit -m "feat: build reviewable chat starter and CLI"
```

---

### Task 7: Final docs and audit

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update README.md with usage example**

Append to `README.md`:

```markdown
## Example

```powershell
python scripts/build_starter.py --project "EC8 Edge Crew"
# -> starters/pending-review/EC8 Edge Crew - 20260706.md
```

Review the file, add your goal under "Goal for This Chat", then move it to `starters/ready-to-paste/`. Paste the contents into a new Kimi or Claude chat.
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add usage example to README"
```

---

## Self-Review Checklist

**Spec coverage:**
- External twin profile docs: Task 1.
- Read kimi-chat-scraper profiles: Tasks 4 and 6.
- Read Lares canonical profile: Tasks 3 and 6.
- Read Lares domain-pack markdown summaries: Tasks 5 and 6.
- Project-to-domain mapping: Tasks 1 and 2.
- Generate markdown starter: Task 6.
- Write to `pending-review/`: Task 6.
- Simple CLI (`--project` or interactive): Task 6.
- No giant `.json` reads: enforced by only reading `.md` files.
- No auto-promotion or auto-send: output goes to `pending-review/` only.

**Placeholder scan:**
- No TBD/TODO in implementation steps.
- Each step includes exact file paths, code, and commands.

**Type consistency:**
- `load_project_domain_map` returns `dict[str, list[str]]`.
- `parse_project_profile` returns `dict[str, str | list[str]]`.
- `read_domain_pack` returns `dict[str, str | list[str]]`.
- `build_starter` returns `Path`.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-07-06-outside-brain-plan.md`.

Two execution options:

1. **Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks.
2. **Inline Execution** — execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
