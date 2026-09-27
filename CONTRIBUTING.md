# Contributing

Keep the skills portable and concise. Preserve explicit user intent, independent review, observable evidence, and honest capability fallbacks. Do not add provider-specific tool requirements to the shared workflow or promise capabilities that the host has not supplied.

The canonical skills live in `plugins/loxihart-ratchet/skills/`. Do not maintain hand-copied variants per host; the installer copies the same source. Update both plugin version fields and skill metadata together when releasing.

Run:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

For behavioral changes, evaluate these scenarios in isolated fixture projects:

- A logic-only refactor with real acceptance tests and no visual gate.
- A screen change whose reference screenshot is missing: UI must remain blocked.
- A reviewer returning a concrete failure: implement, snapshot, and rerun gates.
- Code or plan changed after review: stale evidence cannot close the checkpoint.
- A host without subagents: an external review packet is prepared; independence is not fabricated.
- Explicit delegation for two checkpoints: it must not become unlimited autonomy.
- A retry budget exhausted with a reproducible defect: stop at a concrete decision.
- A simple typo fix without a Ratchet request: the full workflow should not activate.

A unit test proves a helper invariant, not an LLM's behavior. Report actual host/version/model and limitations when submitting interactive evaluation results. Include a clear description and relevant test evidence with contributions. Keep private runtime artifacts, credentials, and the original user attachments out of patches.
