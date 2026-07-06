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
                tmp_path / ".." / ".." / "ACTIVE" / "kimi-chat-scraper" / "profiles" / "EC8 Edge Crew.md",
                "# Profile: EC8 Edge Crew\r\n"
                "Conversations: 2\r\n"
                "\r\n"
                "## Summary\r\n"
                "- **Edge** (account1, 10 messages)\r\n",
            )

            archive = (
                tmp_path / ".." / ".." / "ACTIVE" / "kimi-chat-scraper" / "kimi-chat-archive" / "account1"
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
