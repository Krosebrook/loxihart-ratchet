# A portable interpretation of Ratchet

Shopify describes incremental checkpoints with ordered behavior, UI, adversarial, and engineer gates. Its published system uses specialist tools and reviewers; this project provides portable instructions and a local evidence ledger. [Original account](https://shopify.engineering/helix).

The existing implementation is a useful executable reference for a migration. New features instead need accepted requirements and design references. A checkpoint should have a concrete outcome, a short diff, and enough evidence to decide whether it is correct. There is no universal line-count limit.

## Roles and gates

| Gate | Evidence | Failure response |
| --- | --- | --- |
| Behavior | Acceptance coverage, commands/results, runtime observations | Fix the defect or report the missing capability |
| UI, when applicable | Comparable screenshots and an actual visual review | Correct unintended differences and recapture |
| Adversarial | Two separate reviewer sessions with concrete verdicts | Resolve findings; review the new revision |
| Engineer | Actual approval or explicit delegation covering this checkpoint | Address feedback or wait for the required decision |

One adversarial gate has two records, `review-a` and `review-b`. The human gate must not become an automatic “tests passed” flag. Delegation covers only the scope actually granted and never authorizes unrelated external actions.

## Original implementation choices

This repository adds a default budget of three implementation attempts, JSON reports, SHA-256 content fingerprints, a no-overwrite installer, and conservative invalidation of all gates after any code or plan change. These are design choices here, not claims about Shopify's internal implementation.

The agent orchestrates the loop; the ledger does not execute tests or models. The agent must enforce checkpoint sequencing and delegation limits. Each checkpoint directory is managed by one writer, and concurrent independent work should use separate Git worktrees and checkpoint identifiers. The current helper has no interprocess locking or cross-checkpoint scheduler.

Memory captures accepted decisions with their evidence and scope. It must not turn old preferences into permanent restrictions or expand permission. Bounded autonomy should follow evidence and explicit user intent.

## Applicable beyond mobile

For an API refactor, use response/error contracts and performance measurements; explain why UI review is inapplicable. For a screen migration, align device, data, theme, font scale, and state before comparisons. For a new feature, specify the expected behavior first and validate against it rather than treating generated code as its own specification.

The workflow cannot guarantee correctness or a particular development speed. The quality of the acceptance criteria, runtime tools, and independent reviews determines how useful its evidence is.
