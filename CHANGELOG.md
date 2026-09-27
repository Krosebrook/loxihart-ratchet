# Changelog

## 0.1.0-loxihart.2 (2026-09-25)

One plugin instead of two. Removed `cowork/ratchet/`, which repackaged the same method as a second plugin and duplicated four skill names. The six skills in `plugins/loxihart-ratchet/` are the slash commands in Claude Code and Cowork, so no legacy `commands/` folder is needed. The marketplace `renames` map moves existing `ratchet` installs to `loxihart-ratchet`. README now lists the slash commands and no longer places the Codex sentence inside the Cowork paragraph. No changes to skills, ledger, installer, or tests.

## 0.1.0-loxihart.1 (2026-09-24)

Forked from jaleco8/helix-skills 0.1.0 (commit 25ff07b). Renamed Helix to Ratchet across skills, plugin, ledger (`.ratchet/`), installer, and docs; rebranded manifests to Loxihart (Abstrekkt); pointed install and marketplace commands at Krosebrook/loxihart-ratchet. No behavioral changes to the skills, ledger, or installer. Added `cowork/ratchet/`, a Cowork plugin packaging (five commands, five skills; behavior and UI merged into `ratchet-verify`), registered in the marketplace. Upstream history below.

## 0.1.0 — 2026-09-24

Initial community implementation: six portable skills, Codex and Claude plugin manifests, Claude marketplace, nine host installation targets, checkpoint evidence ledger, bilingual entry documentation, usage examples, and automated validation.

Host discovery paths are documentation-backed. Full interactive runs across every host remain unverified.
