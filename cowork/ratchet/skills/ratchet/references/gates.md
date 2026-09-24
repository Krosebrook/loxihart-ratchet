# Gate contract and manual fallback

For the current checkpoint, preserve the plan, reference, acceptance criteria, implementer session, revision identifier, and authorization scope. Use the helper's fingerprint when available; a manual revision must be labeled manual and tied to an inspectable diff/commit.

Each report contains gate, revision, verdict, actor, actual session identifier, summary, unresolved findings, and evidence artifacts. Verdicts are `pass`, `fail`, or `blocked`. A passing report has no unresolved findings. Accepted tradeoffs need explicit reasoning and scope in the summary, not erased history.

1. Behavior: each acceptance criterion has an observed result and repeatable procedure. Keep command output, exit code, environment, and coverage.
2. UI: comparable reference/candidate screenshots were actually inspected. Record setup, states, differences, and limitations. Only logic-only changes can omit this gate with a specific plan reason.
3. Adversarial: two independent sessions review the same revision. Record initial verdicts separately and keep actual reviewer reports. The implementer cannot provide either independent verdict. Reviewers may share a model but not the implementation context or each other's initial conclusions.
4. Approval: preserve the engineer's actual message or the prior explicit delegation covering this checkpoint. Record authority as `human` or `explicit-delegation`; a fabricated transcript or blanket inference from “implement this” is invalid.

If any gate fails, correct the implementation and rerun checks for the new revision. Missing tools leave a gate blocked. Keep history and bounded retry accounting. At the retry limit, present the issue and a concrete next decision rather than looping indefinitely.

For manual operation, put the same information in Markdown files under `.ratchet/`, track each artifact and revision explicitly, and disclose that automated freshness checks did not run. Do not mark the whole checkpoint complete while any applicable gate is missing. The process is only as trustworthy as its observations and reviewers.
