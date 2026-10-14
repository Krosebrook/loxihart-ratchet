---
name: ratchet-ui-review
description: Compare reference and candidate UI evidence for a Ratchet checkpoint. Use for visual parity or design validation when comparable screenshots and vision capabilities are available.
license: MIT
metadata:
  author: Loxihart (Abstrekkt); upstream jaleco8/helix-skills
  version: "0.1.0-loxihart.2"
---

# Visual review

Establish equivalent viewport/device, display scale, theme, locale, font scale, data, and interaction state. Identify reference and candidate screenshot paths and the checkpoint revision. If capture or image inspection is unavailable, return blocked; do not infer visual correctness from source code.

Inspect hierarchy, spacing, alignment, typography, colors, icons, clipping, content density, and state changes. Compare loading, empty, error, and interaction states only as relevant to the checkpoint. Identify intended platform differences before calling them regressions. Screenshots alone do not prove accessibility: pair with semantic/tree inspection or runtime checks for labels, focus order, and touch targets when in scope.

Prefer an independent visual reviewer and use the actual available vision model; this skill does not call Gemini or another service automatically. Do not claim pixel equivalence from subjective inspection or use an arbitrary global similarity percentage as the only oracle.

Return gate `ui`, revision, actor/session, verdict, compared states and image paths, specific actionable differences, and known limitations. Link each finding to a region/state and acceptance criterion. Archive the captures and review. If there is no UI change, the plan must state why the gate is inapplicable; lack of tools is not that reason. After a correction, capture and review the updated implementation.
