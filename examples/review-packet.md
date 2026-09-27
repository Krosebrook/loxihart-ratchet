# Independent reviewer request

Use `ratchet-adversarial-review` in a fresh session. Review this checkpoint without modifying code. Do not inspect the other reviewer's initial verdict.

The implementer supplies:
- The actual checkpoint plan and acceptance criteria.
- The exact content revision, baseline commit, and diff.
- Source/design reference and applicable repository architecture guidance.
- Behavior and applicable UI evidence, with their runtime setup.
- One assigned gate: `review-a` or `review-b`.

Check correctness, boundaries, architecture, and acceptance coverage. Return a report using the ledger contract, with your actual actor/session, observed findings, and evidence paths. Do not pass based only on the implementer's summary. If you lack the code or runtime needed to assess a criterion, identify that limitation. A different role label inside the implementation conversation is not a fresh session.
