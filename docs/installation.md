# Installation

Clone this repository and run `scripts/install.py` from the clone. Python 3.10+ is enough; the installer performs no network requests and does not execute repository hooks.

```bash
python3 scripts/install.py --agent codex --project /absolute/path/to/project --dry-run
python3 scripts/install.py --agent codex --project /absolute/path/to/project
```

The project must already exist. Choose the agent you actually use. Repeat `--agent` to install for multiple hosts; destinations shared by Codex, Antigravity, and Kimi are deduplicated. Avoid installing the same skills through both a plugin and a directory in the same host; duplicate discovery varies by host.

The installer copies the six directories from `plugins/loxihart-ratchet/skills/` into the documented native location. It does not edit `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, agent settings, shell profiles, or credentials. It is idempotent for identical files and checks all collisions before copying. Filesystem errors during copying may leave a partial install: inspect the reported destination before retrying.

Restart or refresh the host's skill list if changes are not discovered. Ask it to load `ratchet` by name. In Codex use `$ratchet`; in Claude directory mode use `/ratchet`; in Claude plugin mode use `/loxihart-ratchet:ratchet`.

## Plugin distribution

`plugins/loxihart-ratchet/` is a self-contained plugin root with `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, `skills/`, and a license. The repository root is a Claude marketplace, not a plugin root.

Claude Code:

```text
/plugin marketplace add Krosebrook/loxihart-ratchet
/plugin install loxihart-ratchet@loxihart-ratchet
```

For a local Claude test, launch `claude --plugin-dir /absolute/path/to/loxihart-ratchet/plugins/loxihart-ratchet`.

For Codex, the tested installation path in this repository is the project skill installer. The bundled manifest is available for plugin distribution, but this release has not been submitted to or verified in an official Codex marketplace. No personal marketplace is changed by the installer.

## Upgrades and removal

Pull a reviewed release or commit into this clone and run the installer with `--dry-run`. If installed content differs, it refuses to overwrite it. Back up custom changes, remove only the six `ratchet*` directories previously installed, and rerun the installer. Do not delete the parent skills directory or other skills. Plugin installations should be updated or uninstalled through their host plugin manager.

Removing skills does not remove the target project's `.ratchet/` evidence. Keep or archive that data separately according to your project policy.

## Runtime evidence

Before the first snapshot, add `.ratchet/` to the target project's `.gitignore` or local `.git/info/exclude` with the project's normal permission rules. The installer does not change these files. The ledger always excludes `.ratchet/` from its fingerprint to avoid invalidating a revision when evidence is written, but that exclusion does **not** stop Git from publishing the directory.

Use the helper in the installed `ratchet/scripts/` directory, passing an absolute `--project` path. Never place application code under `.ratchet/`; that directory is exclusively evidence and workflow state.
