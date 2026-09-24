# UI Review Gate Reference

## Setup parity

Before comparing, match all of the following between reference and candidate:

- Viewport or device model, and display scale
- Theme (light or dark), locale, and font scale
- Data fixtures and account state
- Interaction state (scroll position, expanded sections, focused field, open modal)

If the two captures show different sections or states (for example one shows an
unfulfilled order and the other a fulfilled order), mark the comparison INVALID,
recapture both in the same state, and compare again. An INVALID comparison is not a
pass and not a fail.

## Scope to the checkpoint

Compare only what the current checkpoint built. For a skeleton checkpoint, check only
the navigation bar and title even though the reference shows a full screen. The scope
grows with each checkpoint.

## Inspection checklist

- Hierarchy and structure
- Spacing, margins, and padding (judge sizes proportionally to each screenshot's dimensions)
- Alignment
- Typography: size, weight, and line height
- Colors and dividers
- Icons
- Clipping and truncation
- Content density
- State changes: loading, empty, error, and interaction, only where relevant to the checkpoint

Identify intended platform differences before calling them regressions, and record
them as accepted with a reason.

## Findings

List every difference found. Each finding includes a severity, an on-screen location,
the state it appears in, and the acceptance criterion it affects. Any visual difference
that can be fixed in code is a blocker by default.

## Limits

- Do not claim pixel equivalence from subjective inspection.
- Do not use a global similarity percentage as the only oracle.
- Screenshots alone do not prove accessibility. When accessibility is in scope, pair
  them with semantic tree inspection or runtime checks for labels, focus order, and
  touch targets.
- If there is no UI change, the plan must say why the gate is inapplicable. Lack of
  tools is not that reason; it makes the gate blocked.
- After any correction, recapture and review the updated implementation.

## Background

Shopify's published Helix method uses a vision model acting as a perfectionist design
reviewer, required to list every difference with severity and location. This reference
adopts that contract without assuming a specific model: use whichever vision-capable
model the host actually provides, and record which one in the report's `actor` field.
