import tempfile
import unittest
from pathlib import Path

from scripts.build_starter import build_starter


class TestBuildStarter(unittest.TestCase):
    def _write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_build_starter(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self._write(
                tmp_path / "config" / "project_domain_map.json",
                '{"EC8 Edge Crew": ["betting"]}',
            )
            self._write(
                tmp_path / "profile" / "outside-brain-profile.md",
                "# outside-brain Profile\n\nTwin.\n",
            )

            lares_root = tmp_path / ".." / "lares-profile"
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

            scraper_root = tmp_path / ".." / ".." / "ACTIVE" / "kimi-chat-scraper"
            self._write(
                scraper_root / "profiles" / "EC8 Edge Crew.md",
                "# Profile: EC8 Edge Crew\r\n"
                "Conversations: 5\r\n"
                "\r\n"
                "## Summary\r\n"
                "- **Edge** (account1, 10 messages)\r\n",
            )

            result = build_starter(tmp_path, "EC8 Edge Crew")

            self.assertTrue(result.exists())
            content = result.read_text(encoding="utf-8")
            self.assertIn("EC8 Edge Crew", content)
            self.assertIn("Guardian.", content)
            self.assertIn("Edge crew odds", content)
            self.assertIn("## Confidence Scores", content)
            self.assertIn("pending-review", str(result))
