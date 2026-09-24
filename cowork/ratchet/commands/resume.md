---
description: Record lessons and resume a paused Ratchet run
argument-hint: "[checkpoint-id]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*), Bash(python3:*)
disable-model-invocation: true
---

Record accepted lessons and prepare the handoff for Ratchet checkpoint: $ARGUMENTS

If no checkpoint id was supplied, read `.ratchet/memory.md` in the target repository, report the most recent entry, and ask whether to resume it. Verify the working tree against the recorded snapshot before trusting any earlier green result.

Use the **ratchet-memory** skill for the memory entry format, resume checks, and quality standards.
