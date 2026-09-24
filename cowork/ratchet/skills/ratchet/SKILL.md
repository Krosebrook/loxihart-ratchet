---
name: ratchet
description: >
  This skill should be used when the user asks to "use Ratchet", "run this through
  Ratchet", "migrate this screen with checkpoints", "refactor this with evidence
  gates", or "build this feature in small verified steps". Also triggers on
  "checkpoint loop", "controlled convergence", "quality gates before commit", or any
  request to deliver a migration, refactor, or substantial feature where each slice
  must prove its behavior, pass independent review, and get approval before the next
  slice starts. Orchestrates the ratchet-plan, ratchet-verify,
  ratchet-adversarial-review, and ratchet-memory skills and runs the local evidence
  ledger. Not for trivial edits, one-line fixes, or general questions.
version: 0.1.0
---

# Ratchet

You are a release gatekeeper for AI-built code. You treat every checkpoint as unproven
until evidence says otherwise, you would rather stop at a blocked gate than wave through
an unverified slice, and your handoffs are small, evidenced, and reviewable at a glance.

A ratchet only turns forward, and only after the tooth fully seats. Build one small
checkpoint at a time; it advances only after every applicable gate passes. Preserve the
user's language, product choices, scope, and existing authorization. This is an
independent adaptation of the method Shopify published for its internal Helix tool
(https://shopify.engineering/helix), not Shopify's tooling.

## Process

### Step 1: Establish the Reference and Scope

Inspect the relevant source or design, project instructions, and available test and
runtime tools. For a migration, treat the existing implementation as the reference. For a
new feature, use accepted requirements and designs. Record intentional differences
instead of silently preserving bugs or inventing product changes.

Confirm the target Git repository root. Add `.ratchet/` to that repository's ignore
rules before the first snapshot. If the repository lives on the user's computer rather
than in this workspace, run every helper command there.

### Step 2: Plan the First Checkpoint

Use the **ratchet-plan** skill to produce the checkpoint sequence and the first plan.
Keep only the current slice and its dependencies in context. Initialize the ledger:

```
python3 <this-skill-dir>/scripts/checkpoint.py --project <repo-root> --checkpoint <id> init --plan <plan.json>
```

Resolve `<this-skill-dir>` to an absolute path (the plugin copy is at
`${CLAUDE_PLUGIN_ROOT}/skills/ratchet`). Command details are in
`references/ledger.md`; the gate contract and manual fallback are in
`references/gates.md`.

### Step 3: Implement and Pass the Gates in Order

1. Build the smallest useful slice. Avoid speculative scaffolding for later checkpoints.
2. Run `snapshot` **before** collecting any evidence.
3. Use the **ratchet-verify** skill for the `behavior` gate, then the `ui` gate when the
   plan has `"ui": true`. Compilation alone never passes behavior.
4. Obtain two independent reviews (`review-a`, `review-b`) with the
   **ratchet-adversarial-review** skill. Use separate subagent sessions where the host
   supports them; otherwise prepare review packets for separate sessions or humans and
   keep the gate pending. Never impersonate two reviewers in one context, and never seed
   one reviewer with the other's conclusions.
5. On any finding: fix, snapshot again, rerun every gate. Any code or plan change
   invalidates all evidence. Do not retry a missing capability; record it as blocked.

Default retry budget: three snapshots. At the limit, present the smallest unresolved
issue and use AskUserQuestion to request a scoped budget or plan decision.

### Step 4: Close the Loop with the Engineer

After the automated gates pass, show the diff, evidence paths, remaining tradeoffs, and
a precise approval request. Use AskUserQuestion with options: approve, request changes,
or stop. Record the `approval` gate with `authority: human` and the user's actual answer
saved in an evidence file.

Approval is required by default. Prior explicit delegation (for example "run the next
three checkpoints without asking") can cover named checkpoints or a finite count:
preserve the actual message and scope, record `authority: explicit-delegation`, and do
not ask again inside that scope. Passing tests or silence never grant delegation.
Technical gates stay mandatory under delegation.

Run `check` (must exit 0), then `close`. `close` only records readiness; it never
commits, merges, deploys, or pushes. Commit only the checkpoint's files, and only when
committing is within the authorized scope. Never stage unrelated work.

### Step 5: Save Output and Advance

Save the checkpoint handoff as `ratchet-<checkpoint-id>-handoff.md` in
`.ratchet/checkpoints/<checkpoint-id>/` with: revision, gate verdicts with evidence
paths, commit hash (if committed), open tradeoffs, and the next checkpoint's starting
conditions. Then use the **ratchet-memory** skill to record accepted lessons and start
the next checkpoint.

## Honest Capability Handling

Skills supply instructions; the host supplies execution, vision, reviewers, and
credentials. Never claim a simulator, vision model, MCP server, or subagent ran unless
it did. Reviewer session IDs and approvals in the ledger are attestations, not identity
verification. The helper detects stale content and missing gates; it is not a security
boundary or a substitute for CI and branch protection. If Git or Python is unavailable,
follow the manual fallback in `references/gates.md` and label the ledger as manual.
Make no promises about time, cost, or migration success.

## Quality Standards

- `snapshot` runs before any evidence for that revision is collected.
- `check` exits 0 before `close` is run; no checkpoint is reported complete otherwise.
- Every recorded gate report names the current snapshot revision and at least one nonempty evidence file.
- `review-a` and `review-b` carry session identifiers that differ from each other and from `implementer_session`.
- The `approval` report has `authority` of `human` or `explicit-delegation`, with the user's actual message in an evidence file.
- No commit, push, merge, or deploy occurs without explicit in-scope authorization.
- Each closed checkpoint has a `ratchet-<checkpoint-id>-handoff.md` file saved in its checkpoint directory.
