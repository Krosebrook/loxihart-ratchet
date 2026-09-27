# Local evidence ledger

Python 3.10+ and Git are required. Resolve `scripts/checkpoint.py` relative to the installed `ratchet` skill directory. All commands require a target Git repository root and unique checkpoint slug:

```text
python3 /absolute/path/to/ratchet/scripts/checkpoint.py \
  --project /absolute/path/to/project --checkpoint cp-01 COMMAND
```

| Command | Effect |
| --- | --- |
| `init --plan /path/to/plan.json` | Validate and copy a plan; refuse existing checkpoint |
| `snapshot` | Start an attempt, hash current project content and plan, clear active gates |
| `record --report /path/to/report.json` | Archive an actual gate report and hash its evidence |
| `status` | Display missing/stale gates (always exit 0 for a valid ledger) |
| `check` | Exit 0 only if every applicable gate is currently valid; otherwise 1 |
| `close` | Mark a fully verified checkpoint closed; never commit or publish |

Operational/input errors exit 2. Attempts count snapshots, not individual gate invocations. The default plan allows three attempts. Budget changes alter the plan and require new evidence; make them only following the user's scoped decision.

## Plan

Use `assets/plan.json` as a shape example. Replace its title, reference, acceptance criteria, implementer session, and UI applicability with actual values. `ui: false` requires a `ui_skip_reason`. `max_attempts` must be an integer from 1 to 20. Optional plan fields can hold architecture constraints, reference commit, dependencies, and approval scope; the helper hashes them but does not enforce their semantics.

The plan is copied to `.ratchet/checkpoints/<id>/plan.json`. Edit that copy when a plan correction is authorized. Store runtime evidence only under its `evidence/` directory.

## Report

A report must include these fields (the values below describe the shape; they are not evidence):

```json
{
  "gate": "behavior",
  "revision": "the-current-snapshot-sha256",
  "verdict": "pass",
  "actor": "actual-tool-or-reviewer",
  "session": "actual-session-id",
  "summary": "Which acceptance criteria were demonstrated and how",
  "findings": [],
  "artifacts": ["evidence/behavior.log"]
}
```

Allowed gate order: `behavior`, `ui` (if applicable), `review-a`, `review-b`, `approval`. Approval reports additionally need `authority: human` or `authority: explicit-delegation`, with the actual decision and scope in an evidence file. Record a fail/blocked verdict at the earliest failing gate; downstream gates cannot advance until it passes.

Save report inputs under the checkpoint's `evidence/` directory as well, so creating them does not change the project snapshot. Artifact paths are relative to the checkpoint directory and must resolve to nonempty files inside `evidence/`. Use descriptive names, preserve raw observations, and redact secrets before any sharing.

Replacing a gate invalidates its downstream records. Old reports remain archived in `reports/` and history stays in `state.json`. Changes to code or plan require a new snapshot and fresh gate reports. Changes to referenced artifacts or archived reports make that gate stale.

## Boundaries

The fingerprint includes tracked files and nonignored untracked files (content, executable status, symlink target, and deletions), plus the plan. It excludes `.ratchet/`. Git-ignored data, external services, dependency contents, environment variables, and symlink target contents are not fingerprinted. Record versions/configuration/fixtures in evidence; rerun checks when those inputs change. Submodule directory entries are rejected; review a submodule in its own checkpoint and validate integration separately.

Use one writer per checkpoint. There is no cross-process locking, scheduler, automatic test runner, cryptographic identity, authenticated approval, or malicious-tamper protection. State is editable JSON. The helper verifies declared identities are different; it cannot prove independence. `closed` is a historical marker: later changes can make the current `check` fail while that marker remains true. Create a new checkpoint for follow-up work and preserve the accepted commit/diff in the handoff.
