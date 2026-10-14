---
name: ratchet-plan
description: Break a migration, refactor, or feature into observable Ratchet checkpoints. Use before implementation when checkpoint scope, reference behavior, or acceptance evidence is unclear.
license: MIT
metadata:
  author: Loxihart (Abstrekkt); upstream jaleco8/helix-skills
  version: "0.1.0-loxihart.2"
---

# Plan a Ratchet checkpoint

Read only the relevant reference and architecture constraints. Produce a short ordered sequence of independently reviewable slices, then detail the first. Prefer a working vertical slice over infrastructure that cannot yet demonstrate behavior. Existing software is evidence of behavior, not permission to reproduce an acknowledged defect.

For each checkpoint define:
- A user-visible or measurable outcome, reference location/version, dependencies, and out-of-scope behavior.
- Concrete acceptance examples: starting state, action/input, expected output, and observable proof. Include error/empty/loading cases when they belong to this slice.
- UI applicability; for logic-only work give a specific reason for skipping visual review.
- Architecture constraints, relevant analytics/accessibility/data contracts, and any performance threshold with a repeatable measurement.
- The behavior command or manual procedure, visual capture setup if applicable, and reviewer packet contents.
- A bounded retry budget and the current authorization for engineer approval. Do not infer autonomy from a broad request to implement.

Use the template bundled with `ratchet` when installed; otherwise write equivalent JSON or Markdown. The plan must be small enough to assess without reading a future implementation. Do not demand a separate planning approval unless the project or user requires it. Reuse authorization already given. Changes to acceptance criteria require an explicit explanation; never weaken them merely to make a failing implementation pass.

Example: first preserve pagination for a read endpoint with boundary tests; add caching in a later checkpoint with invalidation tests. For a screen migration, first verify navigation and one data section, then add the remaining states and interactions.
