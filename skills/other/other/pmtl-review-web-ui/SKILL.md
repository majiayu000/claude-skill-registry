---
name: pmtl-review-web-ui
description: PMTL_VN frontend review skill. Use when reviewing UI, accessibility, interaction quality, redesign opportunities, or web interface compliance. Prioritize findings over summaries and anchor review comments in PMTL visual and behavioral standards.
---

# PMTL Review Web UI

## Purpose

Review PMTL web interfaces for interaction, accessibility, composition, and visual quality with findings-first output.

## Use When

- The task is a UI review, UX audit, or design quality check.
- You need concrete frontend findings tied to PMTL standards.

## Required Inputs

- target route, component, screenshot, or implementation files
- whether the task is review-only or expected to lead into fixes
- any PMTL owner docs that define the intended behavior or visual standard

## Expected Output

- Findings-first review output with concrete user-facing consequences.
- Tight file references and a brief summary only after the findings.

## Review order

1. Identify the target route, component, or feature.
2. Read nearby implementation files first.
3. Check behavior with `pmtl-ui-behavior`.
4. Check visual hierarchy with `pmtl-ui-style-system`.
5. Check performance-sensitive patterns with `vercel-react-best-practices` when relevant.

## Execution Approach

1. Inspect the implemented surface and nearby dependencies.
2. Identify broken behavior before discussing aesthetics.
3. Prioritize findings that block usability, accessibility, or trust.
4. Keep the summary brief after findings.

## Findings to prioritize

- Broken interaction cycles: loading, empty, error, focus, submit, disabled, success.
- Accessibility violations and keyboard traps.
- Layouts that feel generic, crowded, or inconsistent with PMTL's editorial tone.
- Weak component composition when `shadcn` primitives should have been reused.
- Visual regressions on mobile, especially around height, density, and spacing.

## Output rule

Present findings first, with file and line references. Keep summary brief.

## Verification

- Every finding should point to a concrete user-facing consequence.
- Avoid style-only opinions when behavior or accessibility failures are more severe.
- Findings should be reproducible from the current implementation or current screenshots/surfaces.
- Tie each finding to PMTL behavior or visual standards instead of generic taste claims.

## Quality Criteria

- Severity tracks actual user harm, not reviewer preference.
- Behavior, accessibility, and trust issues outrank surface polish.
- Review stays within web/UI scope and does not drift into backend/API/data claims without evidence.

## Edge Cases

- Legacy surfaces may be structurally constrained; still call out user harm first, then note the structural constraint.
- A design can be visually refined but still fail due to broken loading/error/focus cycles.
- Do not use this skill for backend/API/data-layer review; escalate to the appropriate lane instead.

## References

- `pmtl-ui-behavior`
- `pmtl-ui-style-system`
- `vercel-react-best-practices`

## Pair with

- `pmtl-fe-implementation` when the review is expected to lead directly into code changes.
- `pmtl-verify-quality-gate` after the reviewed fixes land.
