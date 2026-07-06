import tempfile
import unittest
from pathlib import Path

from scripts.profile_reader import read_profile_section


class TestProfileReader(unittest.TestCase):
    def test_read_profile_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            profile_dir = tmp_path / "profile"
            profile_dir.mkdir()
            (profile_dir / "lares-profile.md").write_text(
                "# Lares Profile\n\n## Persona\nGuardian.\n",
                encoding="utf-8",
            )

            result = read_profile_section(tmp_path, "lares-profile", "Persona")

            self.assertIn("Guardian.", result)

    def test_read_profile_section_crlf(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            profile_dir = tmp_path / "profile"
            profile_dir.mkdir()
            (profile_dir / "lares-profile.md").write_bytes(
                b"# Lares Profile\r\n\r\n## Persona\r\nGuardian.\r\n"
            )

            result = read_profile_section(tmp_path, "lares-profile", "Persona")

            self.assertIn("Guardian.", result)
