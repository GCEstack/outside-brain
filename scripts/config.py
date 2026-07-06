import json
from pathlib import Path


def load_project_domain_map(project_root: Path) -> dict[str, list[str]]:
    config_path = project_root / "config" / "project_domain_map.json"
    return json.loads(config_path.read_text(encoding="utf-8"))
