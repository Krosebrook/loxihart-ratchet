---
name: ratchet-adversarial-review
description: Independently challenge a Ratchet checkpoint for defects, architecture drift, and missing cases. Use as either of two separate reviewer sessions after behavior and applicable UI checks pass.
license: MIT
metadata:
  author: Loxihart (Abstrekkt); upstream jaleco8/helix-skills
  version: "0.1.0"
---

# Independent adversarial review

Receive the reference, checkpoint plan, exact snapshot/diff, repository architecture guidance, and evidence. Review in a context separate from the implementer. Two passes by the implementer are self-review, not two independent reviewers. If assigned both reviewer roles in one session, report the independence limitation and prepare a second review packet.

Read surrounding callers and contracts when needed. Seek concrete defects in state/error handling, data integrity, security boundaries, concurrency, duplication, ownership, performance, and accessibility as relevant. Focus on consequences, not style preferences. Identify acceptance criteria not actually demonstrated by the evidence. Existing project guidance takes precedence over invented architecture rules.

Do not modify code during the review. Do not read the other reviewer's findings before issuing your initial verdict. Both reviewers may use the same model, but must be independent sessions. Report reproducible findings with file/line, trigger, consequence, severity, and suggested verification. Return `pass` only when no unresolved actionable findings remain; distinguish accepted tradeoffs from bugs. Never invent a finding just to satisfy an adversarial role.

Return gate `review-a` or `review-b`, the snapshot revision, actual actor and session identity, verdict, summary, findings array, and report artifacts. If the host cannot create separate sessions, supply this packet for an external agent or human reviewer and leave the gate pending. Fixes require fresh evidence and fresh review for the new revision.
