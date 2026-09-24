---
description: Break a change into small Ratchet checkpoints
argument-hint: "[change or reference to plan]"
allowed-tools: Read, Write, Glob, Grep, Bash(git:*)
disable-model-invocation: true
---

Plan Ratchet checkpoints for: $ARGUMENTS

If no change was supplied, ask what is being migrated, refactored, or built and where its reference lives. Produce the ordered checkpoint sequence and a fully specified first checkpoint. Do not implement anything.

Use the **ratchet-plan** skill for slicing rules, the acceptance-criteria format, and quality standards.
