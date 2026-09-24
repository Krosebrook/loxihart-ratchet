---
description: Run a change through the full Ratchet checkpoint loop
argument-hint: "[change to migrate, refactor, or build]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*), Bash(python3:*)
disable-model-invocation: true
---

Deliver this change through the Ratchet checkpoint loop: $ARGUMENTS

If no change was supplied, ask for the target (a screen, module, endpoint, or feature), its reference (existing code, design, or accepted requirements), and the Git repository root before doing anything else.

The ledger helper lives at `${CLAUDE_PLUGIN_ROOT}/skills/ratchet/scripts/checkpoint.py`. Run it against the target repository root, never against the plugin directory.

Use the **ratchet** skill for the loop, gate order, retry budget, approval rules, and quality standards.
