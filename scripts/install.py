#!/usr/bin/env python3
"""Install Ratchet skills into a project's native skill directory, without dependencies."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugins" / "loxihart-ratchet" / "skills"
TARGETS = {
    "codex": ".agents/skills",
    "claude": ".claude/skills",
    "gemini": ".gemini/skills",
    "antigravity": ".agents/skills",
    "grok": ".grok/skills",
    "opencode": ".opencode/skills",
    "kimi": ".agents/skills",
    "qwen": ".qwen/skills",
    "copilot": ".github/skills",
    "portable": ".agents/skills",
}


def tree(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}


def install(project, agents, dry_run=False):
    project = Path(project).expanduser().resolve()
    if not project.is_dir():
        raise ValueError("Project must already exist")
    sources = sorted(p for p in SOURCE.iterdir() if (p / "SKILL.md").is_file())
    if not sources:
        raise ValueError("No source skills found")
    pending = []
    for relative in sorted({TARGETS[a] for a in agents}):
        for source in sources:
            destination = project / relative / source.name
            if not destination.resolve().is_relative_to(project):
                raise ValueError("Destination symlink escapes the project: " + str(destination))
            if destination.is_symlink():
                raise ValueError("Refusing to replace symlink: " + str(destination))
            if destination.exists():
                if not destination.is_dir() or tree(destination) != tree(source):
                    raise ValueError("Existing skill differs; back it up and remove it before upgrading: " + str(destination))
            else:
                pending.append((source, destination))
    # Check every collision before making any changes.
    for source, destination in pending:
        print(("Would install " if dry_run else "Installing ") + str(destination))
        if not dry_run:
            shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    if not pending:
        print("All requested skills are already installed and match this version.")
    return len(pending)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", action="append", choices=TARGETS, required=True)
    parser.add_argument("--project", required=True, help="Existing destination project")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        install(args.project, args.agent, args.dry_run)
    except (ValueError, OSError) as error:
        print("ratchet-install: " + str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
