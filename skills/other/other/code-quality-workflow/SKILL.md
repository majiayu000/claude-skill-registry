---
name: code-quality-workflow
description: Use when assessing or improving code quality, maintainability, performance, or security hygiene - provides workflows for analysis, code review, and systematic improvements with validation steps.
---

# Code Quality Workflow

## Overview
Standardize how to analyze, review, and improve code quality. This skill centralizes quality assessment, code review practices, and systematic improvements with validation gates.

## When to Use
- Quality assessment or code analysis requests
- Code review (PRs, refactors, pre-merge checks)
- Maintainability or performance improvements
- Security hygiene improvements (non-audit level)

Avoid when:
- A full security audit is required (use security-specific skills)
- The task is purely dependency or artifact cleanup (use repo-cleanup)

## Quick Reference

| Task | Load reference |
| --- | --- |
| Code analysis | `skills/code-quality-workflow/references/analyze-code.md` |
| Code review | `skills/code-quality-workflow/references/code-review.md` |
| Systematic improvements | `skills/code-quality-workflow/references/quality-improve.md` |

## Workflow
1. Select the mode: analyze, review, or improve.
2. Load the matching reference file for the expected structure.
3. Inspect code and identify findings or opportunities.
4. Apply changes (if improving) with safety validation.
5. Verify with tests or lint as appropriate.
6. Report findings, fixes, and follow-ups.

## Output
- Findings or improvements summary
- Validation evidence or recommended checks
- Follow-up backlog items if needed

## Common Mistakes
- Skipping severity prioritization
- Mixing review and improvement without sign-off
- Applying fixes without baseline tests
- Overlapping with full security audit scopes
