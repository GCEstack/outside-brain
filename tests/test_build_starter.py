import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_starter import build_starter


class TestBuildStarter(unittest.TestCase):
    def _write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _project_root(self, tmp: str) -> Path:
        # Mirror the real repo layout so relative lookups resolve under
        # a single isolated temp directory.
        return Path(tmp) / "Projects" / "PERSONAL" / "outside-brain"

    def _write_common_fixtures(self, project_root: Path) -> Path:
        """Create the config, profile, lares, and scraper profile fixtures."""
        self._write(
            project_root / "config" / "project_domain_map.json",
            '{"EC8 Edge Crew": ["betting"]}',
        )
        self._write(
            project_root / "profile" / "outside-brain-profile.md",
            "# outside-brain Profile\n\nTwin.\n",
        )

        lares_root = project_root.parent / "lares-profile"
        self._write(
            lares_root / "profile" / "lares-profile.md",
            "# Lares Profile\n\n## Persona\nGuardian.\n",
        )
        self._write(
            lares_root / "profile" / "lares-voice.md",
            "# Lares Voice\n\nDirect.\n",
        )
        self._write(
            lares_root / "profile" / "lares-memory.md",
            "# Lares Memory\n\nDomain packs linked.\n",
        )
        self._write(
            lares_root / "extracted" / "by-domain" / "betting.md",
            "# Lares — Betting Threads\n\n"
            "- **Thread count:** 744\n"
            "- **Route:** ec4-edge-crew-notes\n\n"
            "## Sources\n\n"
            "- Apps: claude, kimi\n\n"
            "## Thread snippets\n\n"
            "- `/a`: Edge crew odds...\n",
        )

        scraper_root = project_root.parent.parent / "ACTIVE" / "kimi-chat-scraper"
        self._write(
            scraper_root / "profiles" / "EC8 Edge Crew.md",
            "# Profile: EC8 Edge Crew\r\n"
            "Conversations: 5\r\n"
            "\r\n"
            "## Summary\r\n"
            "- **Edge** (account1, 10 messages)\r\n",
        )
        return scraper_root

    def test_build_starter(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self._project_root(tmp)
            self._write_common_fixtures(project_root)

            result = build_starter(project_root, "EC8 Edge Crew")

            self.assertTrue(result.exists())
            content = result.read_text(encoding="utf-8")
            self.assertIn("EC8 Edge Crew", content)
            self.assertIn("Guardian.", content)
            self.assertIn("Edge crew odds", content)
            self.assertIn("## Confidence Scores", content)
            self.assertIn("pending-review", str(result))

    def test_pipe_in_table_cells_is_escaped(self):
        """Pipes in titles and snippets must be escaped for markdown tables."""
        with tempfile.TemporaryDirectory() as tmp:
            project_root = self._project_root(tmp)
            scraper_root = self._write_common_fixtures(project_root)

            archive = scraper_root / "kimi-chat-archive" / "account1"
            self._write(
                archive / "2026-07-03 - Edge Picks" / "chat.json",
                json.dumps({
                    "id": "c5",
                    "title": "Edge | Picks",
                    "created_at": "2026-07-03T06:00:00Z",
                    "messages": [
                        {"role": "user", "content": "odds | value"},
                    ],
                }),
            )

            result = build_starter(project_root, "EC8 Edge Crew")
            content = result.read_text(encoding="utf-8")

            self.assertIn("| Edge \\| Picks |", content)
            self.assertIn("| odds \\| value |", content)
