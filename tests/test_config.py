import json
import tempfile
import unittest
from pathlib import Path

from scripts.config import load_project_domain_map


class TestConfigLoader(unittest.TestCase):
    def test_load_project_domain_map(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config_dir = tmp_path / "config"
            config_dir.mkdir()
            config_path = config_dir / "project_domain_map.json"
            config_path.write_text(
                json.dumps({"EC8 Edge Crew": ["betting", "ec"]}),
                encoding="utf-8",
            )

            result = load_project_domain_map(tmp_path)

            self.assertEqual(result, {"EC8 Edge Crew": ["betting", "ec"]})
