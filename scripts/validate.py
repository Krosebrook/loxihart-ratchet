#!/usr/bin/env python3
"""Validate the distributable skills, manifests, and local Markdown links."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    plugin = root / "plugins/loxihart-ratchet"
    manifests = [json.loads((plugin / name / "plugin.json").read_text(encoding="utf-8"))
                 for name in (".codex-plugin", ".claude-plugin")]
    for manifest in manifests:
        if manifest["name"] != plugin.name or manifest.get("license") != "MIT":
            errors.append("Plugin identity/license mismatch")
    if len({m["version"] for m in manifests}) != 1:
        errors.append("Plugin versions disagree")
    version = manifests[0]["version"]
    skills = sorted((plugin / "skills").glob("*/SKILL.md"))
    if len(skills) != 6:
        errors.append("Expected all six distributable skills")
    for path in skills:
        content = path.read_text(encoding="utf-8")
        if not content.startswith("---\n") or "\n---\n" not in content[4:]:
            errors.append(str(path) + ": invalid frontmatter")
            continue
        front, body = content[4:].split("\n---\n", 1)
        data = yaml.safe_load(front)
        name, description = data.get("name", ""), data.get("description", "")
        if name != path.parent.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append(str(path) + ": invalid name")
        if not isinstance(description, str) or not 1 <= len(description) <= 1024:
            errors.append(str(path) + ": invalid description")
        if not body.strip() or len(content.splitlines()) > 500:
            errors.append(str(path) + ": empty or oversized instructions")
        if data.get("metadata", {}).get("version") != version:
            errors.append(str(path) + ": skill/plugin version mismatch")
        if not (path.parent / "LICENSE").is_file():
            errors.append(str(path) + ": missing standalone license")
        ui = yaml.safe_load((path.parent / "agents/openai.yaml").read_text(encoding="utf-8"))
        if "$" + name not in ui["interface"]["default_prompt"]:
            errors.append(str(path) + ": UI prompt does not identify skill")
    marketplace = json.loads((root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    for entry in marketplace["plugins"]:
        if not (root / entry["source"] / ".claude-plugin/plugin.json").is_file():
            errors.append("Marketplace source does not contain a plugin")
    for path in root.rglob("*.md"):
        if any(part in (".git", ".venv", ".ratchet") for part in path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if target.startswith(("http:", "https:", "#", "mailto:")):
                continue
            local = unquote(target.split("#", 1)[0])
            if local and not (path.parent / local).exists():
                errors.append(f"{path.relative_to(root)}: broken link {target}")
    for path in root.rglob("*.json"):
        if not any(part.startswith(".") and part not in (".codex-plugin", ".claude-plugin")
                   for part in path.relative_to(root).parts):
            json.loads(path.read_text(encoding="utf-8"))
    return errors


if __name__ == "__main__":
    failures = validate()
    print("\n".join(failures) if failures else "Validated six skills, plugin manifests, marketplace, and local links.")
    sys.exit(bool(failures))
