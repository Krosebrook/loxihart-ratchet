---
description: Collect behavior and UI evidence for a checkpoint
argument-hint: "[checkpoint-id]"
allowed-tools: Read, Write, Glob, Grep, Bash(git:*), Bash(python3:*)
disable-model-invocation: true
---

Collect gate evidence for Ratchet checkpoint: $ARGUMENTS

If no checkpoint id was supplied, list the directories under `.ratchet/checkpoints/` in the target repository and ask which one to verify. Run `status` with the ledger helper at `${CLAUDE_PLUGIN_ROOT}/skills/ratchet/scripts/checkpoint.py` first, and stop if the snapshot is stale.

Use the **ratchet-verify** skill for the behavior gate, the UI gate, report format, and quality standards.
