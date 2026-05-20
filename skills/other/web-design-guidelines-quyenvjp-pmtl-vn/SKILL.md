---
name: web-design-guidelines
description: Review UI code for web interface quality, accessibility, and frontend best practices. Compatibility skill kept for existing workflows. Use when asked to review UI, audit design, review UX, or check a PMTL surface against web guidelines.
---

# Web Interface Guidelines

This legacy review skill remains available because older prompts still refer to it.
Prefer `pmtl-review-web-ui` by default.

## Current role

Use this skill as a review entrypoint, then pair it with:

- `pmtl-review-web-ui` for PMTL-specific findings
- `pmtl-ui-behavior` for behavior and accessibility checks
- `vercel-react-best-practices` when the UI review includes performance-sensitive React patterns

## Review output

- findings first
- file and line references
- concise summary only after the findings

If the review depends on external guidelines that may have changed, fetch the current source before finalizing the findings.
