import tempfile
import unittest
from pathlib import Path

from scripts.project_parser import parse_project_profile


class TestProjectProfileParser(unittest.TestCase):
    def test_parse_project_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            profile_path = Path(tmp) / "EC8 Edge Crew.md"
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

            self.assertEqual(result["title"], "EC8 Edge Crew")
            self.assertEqual(result["conversations"], "5")
            self.assertIn("Edge", result["summary"])
