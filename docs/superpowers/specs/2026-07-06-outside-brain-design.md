# outside-brain — Chat Starter Design

**Date:** 2026-07-06  
**Project:** `Projects/PERSONAL/outside-brain`  
**Status:** Design draft — pending Osito/Lares review before implementation  

## Purpose

`outside-brain` is a standalone workspace that turns archived chat history into focused, reviewable chat starters. It sits outside the family system and outside active project repos. It reads from the Kimi chat archive and the Lares port, compacts the relevant context through a project lens, and writes a markdown starter that Osito and Lares review before it is pasted into any new chat.

It is **not** an auto-ingestion pipeline. Every starter is a draft until a human reviews it.

## Scope

### In scope
- Read kimi-chat-scraper project profiles (`Projects/ACTIVE/kimi-chat-scraper/profiles/<project>.md`).
- Read Lares canonical profile docs (`Projects/PERSONAL/lares-profile/profile/`).
- Read Lares domain-pack markdown summaries (`Projects/PERSONAL/lares-profile/extracted/by-domain/<domain>.md`).
- Map project names to Lares domains via a human-editable config.
- Generate one markdown starter per project.
- Write starters to a `pending-review/` folder.
- Provide a simple CLI: `--project` flag or interactive project selection.

### Out of scope
- Reading the giant `.json` domain-pack files (too large; use `.md` summaries only).
- Automatically creating chats inside Kimi, Claude, or any other app.
- Auto-promoting starters to `ready-to-paste/` without human review.
- Modifying source archives or active project files.

## Workspace Structure

```
Projects/PERSONAL/outside-brain/
├── README.md                          # Purpose, quick commands, safety rules
├── docs/superpowers/specs/            # This design doc
├── scripts/
│   └── build_starter.py               # CLI entry point
├── config/
│   └── project_domain_map.json        # project -> Lares domain mapping
├── starters/
│   ├── pending-review/                # Generated starters await review
│   └── ready-to-paste/                # Approved starters
└── tests/
    └── test_build_starter.py
```

## Inputs

| Source | Path | What we use |
|--------|------|-------------|
| Kimi project profile | `Projects/ACTIVE/kimi-chat-scraper/profiles/<project>.md` | Summary section, conversation list, key excerpts |
| Lares persona | `Projects/PERSONAL/lares-profile/profile/lares-profile.md` | Canonical Lares persona |
| Lares voice | `Projects/PERSONAL/lares-profile/profile/lares-voice.md` | Voice/personality notes |
| Lares memory | `Projects/PERSONAL/lares-profile/profile/lares-memory.md` | Domain pack links, facts |
| Lares domain summary | `Projects/PERSONAL/lares-profile/extracted/by-domain/<domain>.md` | Thread count, sources, snippets |

## Project → Domain Mapping

`config/project_domain_map.json` maps a kimi-chat-scraper project name to one or more Lares domain packs.

Initial mapping (editable):

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

## Output Format

Each generated starter is a markdown file named `<project> - <YYYYMMDD>.md`.

Sections:

1. **Project / Focus Header** — project name and date.
2. **Lares Persona & Voice** — copied verbatim from canonical profile docs.
3. **What We've Done Well** — structured excerpts from the project profile's summary/conversation list (no AI summarization; existing text only).
4. **What the Archive Contains** — thread counts, sources, and snippet list from each mapped Lares domain-pack markdown.
5. **Goal for This Chat** — placeholder heading for Osito to fill in before review.
6. **Instructions for the AI** — fixed behavior rules: stay on topic, defer to Osito/Lares, do not invent facts not in the provided context.

## CLI

```powershell
# Direct project
cd Projects/PERSONAL/outside-brain
python scripts/build_starter.py --project "EC8 Edge Crew"

# Interactive — list available projects
python scripts/build_starter.py
```

## Review Gate

1. `build_starter.py` writes to `starters/pending-review/`.
2. Osito and/or Lares read the starter.
3. If approved, move the file to `starters/ready-to-paste/`.
4. Only then is it pasted into a new chat.

No starter is auto-promoted. No starter is pasted by the tool.

## Safety Rules

- This workspace is **external** to active projects and the family system.
- Starters are drafts until reviewed.
- Do not feed a starter back into the archives it was built from.
- Do not use this tool to auto-create or auto-send chats inside any app.

## Open Questions

1. Should `build_starter.py` include a `--goal` flag to seed the "Goal for This Chat" section?
2. Should we add a simple test that verifies a starter is generated for each mapped project?
3. Where should the review approval be logged — in `AUDIT.md`, a `REVIEW_LOG.md`, or by git commit message?
