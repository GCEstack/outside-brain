import json
import tempfile
import unittest
from pathlib import Path

from scripts.confidence_scorer import score_project_conversations


class TestConfidenceScorer(unittest.TestCase):
    def _write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _project_root(self, tmp: str) -> Path:
        # Mirror the real repo layout so relative lookups resolve under
        # a single isolated temp directory.
        return Path(tmp) / "Projects" / "PERSONAL" / "outside-brain"

    def test_score_project_conversations(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self._project_root(tmp)
            self._write(
                project_root / "config" / "project_domain_map.json",
                '{"EC8 Edge Crew": ["betting"]}',
            )
            self._write(
                project_root / ".." / ".." / "ACTIVE" / "kimi-chat-scraper" / "profiles" / "EC8 Edge Crew.md",
                "# Profile: EC8 Edge Crew\r\n"
                "Conversations: 2\r\n"
                "\r\n"
                "## Summary\r\n"
                "- **Edge** (account1, 10 messages)\r\n",
            )

            archive = (
                project_root / ".." / ".." / "ACTIVE" / "kimi-chat-scraper" / "kimi-chat-archive" / "account1"
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

            result = score_project_conversations(project_root, "EC8 Edge Crew")

            self.assertEqual(len(result), 2)
            scores = {r["title"]: r["score"] for r in result}
            self.assertGreater(scores["Edge"], scores["Random"])
            self.assertEqual(result[0]["title"], "Edge")  # sorted high-to-low

    def test_substring_match_does_not_score(self):
        """A keyword that only appears as a substring should score 0."""
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self._project_root(tmp)
            self._write(
                project_root / "config" / "project_domain_map.json",
                '{"EC8 Edge Crew": ["betting"]}',
            )
            self._write(
                project_root / ".." / ".." / "ACTIVE" / "kimi-chat-scraper" / "profiles" / "EC8 Edge Crew.md",
                "# Profile: EC8 Edge Crew\r\n"
                "Conversations: 1\r\n"
                "\r\n"
                "## Summary\r\n",
            )

            archive = (
                project_root / ".." / ".." / "ACTIVE" / "kimi-chat-scraper" / "kimi-chat-archive" / "account1"
            )
            self._write(
                archive / "2026-07-03 - Knowledge" / "chat.json",
                json.dumps({
                    "id": "c3",
                    "title": "Knowledge",
                    "created_at": "2026-07-03T04:00:00Z",
                    "messages": [
                        {"role": "user", "content": "knowledge"},
                    ],
                }),
            )

            result = score_project_conversations(project_root, "EC8 Edge Crew")

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["score"], 0)

    def test_all_keywords_score_one_hundred(self):
        """A chat whose user text contains every project keyword scores 100."""
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self._project_root(tmp)
            self._write(
                project_root / "config" / "project_domain_map.json",
                '{"Alpha Beta": ["gamma"]}',
            )
            self._write(
                project_root / ".." / ".." / "ACTIVE" / "kimi-chat-scraper" / "profiles" / "Alpha Beta.md",
                "# Profile: Alpha Beta\r\n"
                "Conversations: 1\r\n"
                "\r\n"
                "## Summary\r\n",
            )

            archive = (
                project_root / ".." / ".." / "ACTIVE" / "kimi-chat-scraper" / "kimi-chat-archive" / "account1"
            )
            self._write(
                archive / "2026-07-03 - All" / "chat.json",
                json.dumps({
                    "id": "c4",
                    "title": "All",
                    "created_at": "2026-07-03T05:00:00Z",
                    "messages": [
                        {"role": "user", "content": "alpha beta gamma delta"},
                    ],
                }),
            )

            result = score_project_conversations(project_root, "Alpha Beta")

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["score"], 100)
