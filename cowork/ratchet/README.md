# Loxihart Ratchet

**Small checkpoints. Evidence before progress.**

A Cowork plugin that makes Claude deliver migrations, refactors, and substantial
features one small checkpoint at a time. Like a ratchet, work only moves forward once a
checkpoint fully seats: behavior proven, UI matched to the reference, two independent
reviews passed, and an engineer's approval recorded. Every gate writes evidence to a
local ledger that detects stale results.

**Project:** Loxihart (Abstrekkt). Keyword tag: `loxihart`.

## Components

| Type | Name | Purpose |
|------|------|---------|
| Command | `/ratchet:start [change]` | Run a change through the full checkpoint loop |
| Command | `/ratchet:plan [change]` | Produce the checkpoint sequence and first plan only |
| Command | `/ratchet:verify [checkpoint-id]` | Collect behavior and UI gate evidence |
| Command | `/ratchet:review [checkpoint-id] [review-a\|review-b]` | Run one independent adversarial review |
| Command | `/ratchet:resume [checkpoint-id]` | Record accepted lessons and resume safely |
| Skill | `ratchet` | Orchestrates the loop, gate order, retry budget, and approval |
| Skill | `ratchet-plan` | Slices work and writes ledger-ready plans |
| Skill | `ratchet-verify` | Behavior gate, then UI gate when applicable |
| Skill | `ratchet-adversarial-review` | Independent review with reproducible findings |
| Skill | `ratchet-memory` | Evidence-linked lessons and resume checks |
| Script | `skills/ratchet/scripts/checkpoint.py` | Local evidence ledger (init, snapshot, record, status, check, close) |
| Reference | `skills/ratchet/references/ledger.md`, `gates.md` | Ledger commands and gate contract |
| Reference | `skills/ratchet-verify/references/ui-review.md` | UI comparison checklist |
| Reference | `skills/ratchet-plan/references/checkpoint-walkthrough.md` | End-to-end worked example |
| Reference | `skills/ratchet-adversarial-review/references/review-packet.md` | Packet for a separate reviewer session |

Each command delegates to exactly one skill. No MCP connectors are required.

## Setup

- **Python 3.10+** and **Git** on the machine where the target repository lives. The
  ledger uses only the Python standard library and makes no network or model calls.
- The target must be a Git repository. Add `.ratchet/` to its `.gitignore`; the ledger
  excludes that folder from its fingerprint, and it may contain private evidence.
- No environment variables or API keys.
- Optional: a vision-capable model for the UI gate, and subagent support for the two
  independent reviews. Without them, those gates are reported as blocked or pending,
  never passed.

Install: upload `ratchet.plugin` under Personal Plugins in Cowork, or run
`claude plugin install ./ratchet` in Claude Code.

## Usage

```
/ratchet:start Migrate the Orders list screen to the new component library
```

Claude reads the reference, proposes a short checkpoint sequence, and builds the first
slice. It snapshots the repository, then runs the behavior gate, the UI gate if
applicable, and two isolated reviews. It fixes findings and reruns the gates, then asks
you to approve, request changes, or stop. After approval it closes the checkpoint,
writes a handoff and memory entry, and moves to the next slice.

To let it run several checkpoints without asking, say so explicitly, for example "run
the next three checkpoints without approval". That grant is recorded with its scope;
technical gates still apply.

## Output locations (inside the target repository)

| Path | Contents |
|------|----------|
| `.ratchet/plans/` | `ratchet-plan-<id>.json`, `ratchet-plan-sequence.md` |
| `.ratchet/checkpoints/<id>/evidence/` | Gate reports, logs, screenshots, review packets |
| `.ratchet/checkpoints/<id>/` | Ledger state, archived reports, `ratchet-<id>-handoff.md` |
| `.ratchet/memory.md` | Accepted lessons across checkpoints |

## Security

- The ledger never commits, pushes, deploys, or executes commands from reports.
- Commits happen only when committing is within the authorized scope, and only the
  checkpoint's files are staged.
- Reviewer and approval identities in the ledger are attestations, not authentication.
  Use CI and branch protection for enforcement outside the agent.
- Diff content, logs, and documents are treated as untrusted data, never as instructions.
- Keep `.ratchet/` out of public commits; redact secrets before sharing any evidence.

## Provenance

Adapted from [jaleco8/helix-skills](https://github.com/jaleco8/helix-skills) (MIT,
commit `25ff07b`), an independent community implementation of the method Shopify
Engineering published in [Helix: The internal tool powering our Shopify app's native
migration](https://shopify.engineering/helix). Not affiliated with or endorsed by
Shopify. Source repository: `Krosebrook/loxihart-ratchet`. See `LICENSE`.

Changes from upstream: behavior and UI skills merged into `ratchet-verify`, Cowork
commands added, skills restructured to the Cowork plugin format, and output file naming
standardized. The ledger script is unchanged.
