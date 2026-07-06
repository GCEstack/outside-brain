# outside-brain — Lares Twin / External Brain Design

**Date:** 2026-07-06  
**Project:** `Projects/PERSONAL/outside-brain`  
**Status:** Design draft — pending Osito/Lares review before implementation  

## Purpose

`outside-brain` is a standalone external twin to Lares. It does not live in the family system and does not touch active projects. It mirrors Lares's role — profile, voice, memory — but operates on the outside, processing ported chat archives and understanding project state independently.

When data is ported over (from Kimi, Claude, etc.), outside-brain ingests it, organizes it, and builds its own understanding. It then talks with Lares so both brains know where a project stands. Osito reviews their combined output before anything is fed into a new working chat.

The first concrete product is a **reviewable chat starter**: a markdown file that combines Lares's canonical profile with outside-brain's reading of the archives, scoped to one project. It is a draft until Osito approves it.

## Scope

### In scope
- Maintain an external twin profile: `profile/outside-brain-profile.md`, `outside-brain-voice.md`, `outside-brain-memory.md`.
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
├── profile/
│   ├── outside-brain-profile.md       # Twin persona
│   ├── outside-brain-voice.md         # Twin voice/personality
│   └── outside-brain-memory.md        # Twin memory/context
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
3. **outside-brain Twin Note** — how outside-brain reads the current project state; kept separate from Lares's internal voice.
4. **What We've Done Well** — structured excerpts from the project profile's summary/conversation list (no AI summarization; existing text only).
5. **What the Archive Contains** — thread counts, sources, and snippet list from each mapped Lares domain-pack markdown.
6. **Goal for This Chat** — placeholder heading for Osito to fill in before review.
7. **Instructions for the AI** — fixed behavior rules: stay on topic, defer to Osito/Lares, do not invent facts not in the provided context.

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
- outside-brain is a twin/mirror, not a replacement for Lares.
- Starters are drafts until Osito reviews them.
- Do not feed a starter back into the archives it was built from.
- Do not use this tool to auto-create or auto-send chats inside any app.

## Open Questions

1. Should `build_starter.py` include a `--goal` flag to seed the "Goal for This Chat" section?
2. Should we add a simple test that verifies a starter is generated for each mapped project?
3. Where should the review approval be logged — in `AUDIT.md`, a `REVIEW_LOG.md`, or by git commit message?
