# Walkthrough: preserve an API contract during a refactor

This illustrates real usage; it contains no preapproved verdicts. Choose your own target Git repository and actual acceptance criteria.

1. Install the skills for your agent. Add `.ratchet/` to that project's ignore rules before capturing a snapshot.
2. Ask `ratchet-plan` to define a small adapter refactor with observable pagination/error behavior. Use the bundled [plan template](../plugins/loxihart-ratchet/skills/ratchet/assets/plan.json), replacing the sample fields and implementer session. Store the source plan in `/tmp/cp-01-plan.json` or another appropriate local location.
3. Initialize the checkpoint using the installed helper. For Codex's default project installation:

```bash
python3 /path/to/project/.agents/skills/ratchet/scripts/checkpoint.py \
  --project /path/to/project --checkpoint cp-01 init --plan /tmp/cp-01-plan.json
```

4. Implement the bounded refactor. Run `snapshot` with the same `--project` and `--checkpoint` arguments. Retain the returned revision. Execute the actual checks and archive their commands, exit codes, output, and criterion coverage under `.ratchet/checkpoints/cp-01/evidence/`.
5. Write a `behavior` report using the [report contract](../plugins/loxihart-ratchet/skills/ratchet/references/ledger.md), with that revision and the actual evidence paths. Record it:

```bash
python3 /path/to/project/.agents/skills/ratchet/scripts/checkpoint.py \
  --project /path/to/project --checkpoint cp-01 record \
  --report /path/to/project/.ratchet/checkpoints/cp-01/evidence/behavior.json
```

6. For a logic-only adapter, the plan's `ui: false` and specific `ui_skip_reason` omit visual review. If the change actually affects UI, correct the plan, snapshot again, and obtain a real visual review.
7. Give the [review packet](review-packet.md) to two independent sessions. Record the returned `review-a` and `review-b` reports. If either finds a defect, fix it, snapshot again, and rerun all relevant gates.
8. Present the concrete diff and evidence to the engineer. Preserve the real approval or preexisting scoped delegation and record the `approval` report. The helper does not authenticate that message; never synthesize it.
9. Run `check`. It must exit 0 before `close`. Commit only the checkpoint's authorized files and keep the evidence private. Capture the commit and accepted lessons with `ratchet-memory`, then proceed to the next small checkpoint.

If Python/Git, runtime access, reviewers, or approval are unavailable, report precisely which control remains pending. Preparing a packet is useful progress; it is not a passing gate.
