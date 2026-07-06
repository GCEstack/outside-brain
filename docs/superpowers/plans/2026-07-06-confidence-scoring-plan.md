# Confidence Scoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add per-conversation confidence scoring to outside-brain chat starters based on project keyword overlap.

**Architecture:** A new `scripts/confidence_scorer.py` module reads `chat.json` files from the `kimi-chat-scraper` archive, builds a keyword bag per project, and scores each conversation. `scripts/build_starter.py` calls it and renders a "Confidence Scores" table in the generated starter.

**Tech Stack:** Python 3.14, standard library only (`unittest`, `tempfile`, `json`, `re`).

## Global Constraints

- Standard library only; no external dependencies.
- No modifications to `Projects/ACTIVE/kimi-chat-scraper/` or `Projects/PERSONAL/lares-profile/`.
- Read only `.json` chat files from the archive, not raw dumps.

---

### Task 1: Chat archive reader

**Files:**
- Create: `scripts/archive_reader.py`
- Create: `tests/test_archive_reader.py`

**Interfaces:**
- Produces: `read_chat(chat_json_path: Path) -> dict[str, str | list[dict]]`
- Produces: `extract_user_messages(chat: dict) -> list[str]`

- [ ] **Step 1: Write the failing test**

`tests/test_archive_reader.py`:

```python
import json
import tempfile
import unittest
from pathlib import Path

from scripts.archive_reader import extract_user_messages, read_chat


class TestArchiveReader(unittest.TestCase):
    def test_read_chat(self):
        with tempfile.TemporaryDirectory() as tmp:
            chat_path = Path(tmp) / "chat.json"
            chat_path.write_text(
                json.dumps({
                    "id": "chat-1",
                    "title": "Edge",
                    "created_at": "2026-07-03T02:42:08Z",
                    "messages": [
                        {"role": "user", "content": "Edge crew odds today"},
                        {"role": "assistant", "content": "Here are the picks"},
                    ],
                }),
                encoding="utf-8",
            )

            result = read_chat(chat_path)

            self.assertEqual(result["title"], "Edge")
            self.assertEqual(result["created_at"], "2026-07-03T02:42:08Z")
            self.assertEqual(len(result["messages"]), 2)

    def test_extract_user_messages(self):
        chat = {
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi"},
                {"role": "user", "content": "World"},
            ]
        }

        result = extract_user_messages(chat)

        self.assertEqual(result, ["Hello", "World"])
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m unittest tests.test_archive_reader -v
```

Expected: `ModuleNotFoundError`

- [ ] **Step 3: Write minimal implementation**

`scripts/archive_reader.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m unittest tests.test_archive_reader -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/archive_reader.py tests/test_archive_reader.py
git commit -m "feat: read chat.json archives and extract user messages"
```

---

### Task 2: Keyword builder

**Files:**
- Create: `scripts/keyword_builder.py`
- Create: `tests/test_keyword_builder.py`

**Interfaces:**
- Produces: `build_keywords(project_name: str, project_summary: str, domains: list[str]) -> set[str]`
- Produces: `tokenize(text: str) -> set[str]`

- [ ] **Step 1: Write the failing test**

`tests/test_keyword_builder.py`:

```python
import unittest

from scripts.keyword_builder import build_keywords, tokenize


class TestKeywordBuilder(unittest.TestCase):
    def test_tokenize_filters_stop_words_and_punctuation(self):
        result = tokenize("The EC8 Edge Crew picks for today!")
        self.assertIn("ec8", result)
        self.assertIn("edge", result)
        self.assertIn("crew", result)
        self.assertIn("picks", result)
        self.assertNotIn("the", result)
        self.assertNotIn("for", result)

    def test_build_keywords_combines_sources(self):
        result = build_keywords(
            "EC8 Edge Crew",
            "- **Edge** (account1, 10 messages)\n- **Crew picks**",
            ["betting", "ec"],
        )

        self.assertIn("ec8", result)
        self.assertIn("edge", result)
        self.assertIn("crew", result)
        self.assertIn("betting", result)
        self.assertIn("ec", result)
        self.assertIn("picks", result)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m unittest tests.test_keyword_builder -v
```

Expected: `ModuleNotFoundError`

- [ ] **Step 3: Write minimal implementation**

`scripts/keyword_builder.py`:

```python
import re


STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "this", "that",
    "it", "its", "i", "you", "we", "they", "he", "she", "my", "your",
}


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return {w for w in words if w not in STOP_WORDS and len(w) > 1}


def build_keywords(project_name: str, project_summary: str, domains: list[str]) -> set[str]:
    keywords: set[str] = set()
    keywords.update(tokenize(project_name))
    keywords.update(tokenize(project_summary))
    for domain in domains:
        keywords.update(tokenize(domain))
    return keywords
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m unittest tests.test_keyword_builder -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/keyword_builder.py tests/test_keyword_builder.py
git commit -m "feat: build project keyword bag from name, summary, and domains"
```

---

### Task 3: Confidence scorer

**Files:**
- Create: `scripts/confidence_scorer.py`
- Create: `tests/test_confidence_scorer.py`

**Interfaces:**
- Consumes: `read_chat`, `extract_user_messages`, `build_keywords`
- Produces: `score_project_conversations(project_root: Path, project_name: str) -> list[dict[str, str | int]]`

- [ ] **Step 1: Write the failing test**

`tests/test_confidence_scorer.py`:

```python
import json
import tempfile
import unittest
from pathlib import Path

from scripts.confidence_scorer import score_project_conversations


class TestConfidenceScorer(unittest.TestCase):
    def _write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_score_project_conversations(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self._write(
                tmp_path / "config" / "project_domain_map.json",
                '{"EC8 Edge Crew": ["betting"]}',
            )
            self._write(
                tmp_path / ".." / "ACTIVE" / "kimi-chat-scraper" / "profiles" / "EC8 Edge Crew.md",
                "# Profile: EC8 Edge Crew\r\n"
                "Conversations: 2\r\n"
                "\r\n"
                "## Summary\r\n"
                "- **Edge** (account1, 10 messages)\r\n",
            )

            archive = (
                tmp_path / ".." / "ACTIVE" / "kimi-chat-scraper" / "kimi-chat-archive" / "account1"
            )
            self._write(
                archive / "2026-07-03 - Edge" / "chat.json",
                json.dumps({
                    "id": "c1",
                    "title": "Edge",
                    "created_at": "2026-07-03T02:42:08Z",
                    "messages": [
                        {"role": "user", "content": "Edge crew odds today"},
                    ],
                }),
            )
            self._write(
                archive / "2026-07-03 - Random" / "chat.json",
                json.dumps({
                    "id": "c2",
                    "title": "Random",
                    "created_at": "2026-07-03T03:00:00Z",
                    "messages": [
                        {"role": "user", "content": "What is the weather"},
                    ],
                }),
            )

            result = score_project_conversations(tmp_path, "EC8 Edge Crew")

            self.assertEqual(len(result), 2)
            scores = {r["title"]: r["score"] for r in result}
            self.assertGreater(scores["Edge"], scores["Random"])
            self.assertEqual(result[0]["title"], "Edge")  # sorted high-to-low
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m unittest tests.test_confidence_scorer -v
```

Expected: `ModuleNotFoundError`

- [ ] **Step 3: Write minimal implementation**

`scripts/confidence_scorer.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m unittest tests.test_confidence_scorer -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/confidence_scorer.py tests/test_confidence_scorer.py
git commit -m "feat: score conversation confidence per project"
```

---

### Task 4: Integrate confidence scores into starter builder

**Files:**
- Modify: `scripts/build_starter.py`
- Modify: `tests/test_build_starter.py`

**Interfaces:**
- Consumes: `score_project_conversations`

- [ ] **Step 1: Write the failing test update**

In `tests/test_build_starter.py`, after the existing assertions, add:

```python
            self.assertIn("## Confidence Scores", content)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m unittest tests.test_build_starter -v
```

Expected: FAIL — `## Confidence Scores` not found

- [ ] **Step 3: Write minimal integration**

In `scripts/build_starter.py`:

1. Add import:

```python
from scripts.confidence_scorer import score_project_conversations
```

2. After the `## What the Archive Contains` section, add:

```python
    lines.extend([
        "## Confidence Scores",
        "",
        "| Chat | Date | Score | Snippet |",
        "|------|------|-------|---------|",
    ])
    scored = score_project_conversations(project_root, project_name)
    for item in scored:
        date = item["date"][:10] if item["date"] else ""
        lines.append(
            f"| {item['title']} | {date} | {item['score']} | {item['snippet']} |"
        )
    lines.append("")
```

3. Add the new section between "What the Archive Contains" and "Goal for This Chat".

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m unittest tests.test_build_starter -v
```

Expected: PASS

- [ ] **Step 5: Run full test suite**

```bash
python -m unittest discover tests -v
```

Expected: all tests pass

- [ ] **Step 6: Commit**

```bash
git add scripts/build_starter.py tests/test_build_starter.py
git commit -m "feat: render confidence scores in generated starters"
```

---

### Task 5: Regenerate starters and verify

**Files:**
- None (gitignored `starters/pending-review/` output)

- [ ] **Step 1: Regenerate all project starters**

```bash
cd Projects/PERSONAL/outside-brain
python scripts/build_starter.py --project "EC8 Edge Crew"
python scripts/build_starter.py --project "Casa Companion"
python scripts/build_starter.py --project "Heartbeat Family System"
python scripts/build_starter.py --project "Kimi Code Ops"
python scripts/build_starter.py --project "AI Models & APIs"
python scripts/build_starter.py --project "Voice & Audio"
python scripts/build_starter.py --project "Media & Video"
python scripts/build_starter.py --project "Creative & Brand"
python scripts/build_starter.py --project "Desktop & File Org"
```

- [ ] **Step 2: Verify confidence table appears**

```bash
grep -l "## Confidence Scores" starters/pending-review/*.md | wc -l
```

Expected: 9

- [ ] **Step 3: No commit needed**

Starters are gitignored; no commit.

---

## Self-Review Checklist

**Spec coverage:**
- Read chat.json files: Task 1.
- Extract user messages: Task 1.
- Build keyword bag: Task 2.
- Score conversations: Task 3.
- Render confidence table: Task 4.
- Regenerate starters: Task 5.

**Placeholder scan:**
- No TBD/TODO in implementation steps.
- Each step includes exact code and commands.

**Type consistency:**
- `read_chat` returns `dict[str, str | list[dict]]`.
- `extract_user_messages` returns `list[str]`.
- `build_keywords` returns `set[str]`.
- `score_project_conversations` returns `list[dict[str, str | int]]`.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-07-06-confidence-scoring-plan.md`.

Two execution options:

1. **Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks.
2. **Inline Execution** — execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
