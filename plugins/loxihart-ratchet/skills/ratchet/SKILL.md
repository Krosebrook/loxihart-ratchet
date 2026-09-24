---
name: ratchet
description: Deliver migrations, refactors, and substantial features through Ratchet checkpoints and evidence gates. Use when the user requests Ratchet or controlled convergence; avoid for trivial edits or general questions.
license: MIT
metadata:
  author: Loxihart (Abstrekkt); upstream jaleco8/helix-skills
  version: "0.1.0"
---

# Ratchet

Build one small, reviewable checkpoint at a time. Preserve the user's language, product choices, scope, and existing authorization. This is an independent adaptation of Shopify's published method, not Shopify's internal tooling.

## Start from observable intent

Inspect the relevant source or design, project instructions, and available test/runtime tools. For migrations, treat the existing implementation as a reference; for features, use accepted requirements and designs. Record intentional differences instead of silently preserving bugs or inventing product changes.

Use `ratchet-plan` to identify the first bounded checkpoint. If sibling skills are unavailable, use the protocol below and [gates](references/gates.md). Keep only the current slice and its dependencies in context.

Create a plan with [the template](assets/plan.json). Resolve this skill's directory to an absolute path before running `scripts/checkpoint.py --help`; run it against the target Git root, never the plugin checkout by accident. [Ledger usage](references/ledger.md) explains the commands. Store local evidence under `.ratchet/checkpoints/<id>/evidence/`. Exclude `.ratchet/` from public artifacts unless the user deliberately selects and sanitizes them.

## Checkpoint loop

1. State the observable acceptance criteria, affected files, reference, and retry budget (default three implementation attempts). Build the smallest useful slice; avoid speculative scaffolding for later checkpoints.
2. Snapshot the implemented code and plan **before** testing. Collect behavior evidence against the reference with `ratchet-behavior`. Compilation alone is insufficient.
3. For UI changes, use `ratchet-ui-review` with equivalent reference/candidate screenshots and states. For logic-only changes, record why UI is inapplicable in the plan. Missing visual tools means blocked, not inapplicable.
4. Obtain two independent `ratchet-adversarial-review` sessions against the same diff, criteria, and repository guidance. Do not seed one with the other's conclusions. Delegate only where the host and user permit it; otherwise prepare review packets for separate agent or human sessions and keep the gate pending. Never impersonate two reviewers in one context.
5. Fix findings, take a new snapshot, then rerun the gates. Code or plan changes invalidate all evidence in this conservative implementation. Do not repeatedly retry a missing capability; record the blocker. At the retry limit, present the smallest unresolved issue and request a scoped budget/plan decision.
6. After automated gates pass, show the engineer the diff, evidence, remaining tradeoffs, and precise approval request. Approval is required by default. Prior explicit delegation can cover named checkpoints or a finite budget: preserve its actual message and scope, and do not ask again within it. Successful tests or silence never grant delegation. Technical gates remain mandatory.
7. Check the ledger, close the checkpoint, and commit only its authorized changes when committing is within scope. Never stage unrelated work. `close` only records readiness; it does not commit, merge, deploy, or push. Record the commit in the handoff. Then start the next checkpoint.
8. Use `ratchet-memory` to retain validated lessons and resume context. Lessons do not create new permissions or override current user instructions.

## Honest capability handling

Skills provide instructions; the host supplies execution, vision, reviewers, and credentials. Do not claim a simulator, visual model, MCP server, or subagent ran unless it did. Reviewer session IDs and human approvals in the ledger are attestations, not identity verification. The helper detects stale content and missing gates; it is not a security boundary or a substitute for CI/branch protection.

If Git or Python is unavailable, use [manual evidence](references/gates.md) and explicitly label the ledger as manual. If a required runtime, reviewer, or approval is unavailable, finish independent preparation and report the outstanding gate without claiming completion. The package makes no promises about time, performance, cost, or migration success.
