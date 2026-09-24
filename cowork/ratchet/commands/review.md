---
description: Run an independent adversarial checkpoint review
argument-hint: "[checkpoint-id] [review-a|review-b]"
allowed-tools: Read, Write, Glob, Grep, Bash(git:*), Bash(python3:*)
disable-model-invocation: true
---

Review Ratchet checkpoint $1 as reviewer gate $2.

If either argument is missing, ask for the checkpoint id and which gate (`review-a` or `review-b`) this session fills. If this session implemented the checkpoint, do not issue a verdict: prepare the review packet for a separate session and stop.

Use the **ratchet-adversarial-review** skill for independence rules, finding format, and quality standards.
