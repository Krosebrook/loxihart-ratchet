---
name: ratchet-memory
description: Capture accepted Ratchet decisions and prepare checkpoint handoffs. Use after a reviewed checkpoint or when resuming a paused Ratchet run, without converting past feedback into new permissions.
license: MIT
metadata:
  author: Loxihart (Abstrekkt); upstream jaleco8/helix-skills
  version: "0.1.0"
---

# Durable checkpoint memory

Read the last checkpoint plan, verdicts, accepted engineer feedback, and commit/diff. Record a concise entry in the project's local `.ratchet/memory.md`:

- Decision or lesson and its narrow applicability.
- Why it was accepted; link the checkpoint revision, evidence, and actual feedback.
- Known exceptions, remaining issues, and the next checkpoint's starting conditions.
- Current autonomy scope, expiry/checkpoint limit, and the user message that granted it (if any).

Keep observed facts separate from hypotheses. Do not promote an unreviewed suggestion into architecture policy. Do not copy secrets, private payloads, or sensitive screenshots into shared documentation. Propose a sanitized project rule only when the lesson is reusable and within the user's requested scope.

On resume, verify the current working tree against the recorded snapshot. Reopen stale gates after code, plan, or evidence changes; do not trust a previous green summary. Read only memory relevant to the next slice. Past approval does not authorize a new checkpoint, deployment, or external publication beyond its explicit scope.
