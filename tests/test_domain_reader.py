import tempfile
import unittest
from pathlib import Path

from scripts.domain_reader import read_domain_pack


class TestDomainReader(unittest.TestCase):
    def test_read_domain_pack(self):
        with tempfile.TemporaryDirectory() as tmp:
            domain_path = Path(tmp) / "betting.md"
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

            self.assertEqual(result["count"], "744")
            self.assertEqual(result["route"], "ec4-edge-crew-notes")
            self.assertIn("claude", result["sources"])
            self.assertIn("Edge crew odds", result["snippets"])
