---
name: "validate-agents-md"
description: "Validate AGENTS.md files for structural completeness, operational contract coverage, neutrality, and repository alignment."
metadata:
  source_prompt: "prompts/validate-agents-md.prompt.md"
  workflow_type: "validation"
---

# Validate AGENTS.md

## Purpose
Validate `AGENTS.md` files to ensure they are concise, operationally complete, and aligned with repository structure and governance.

## When To Use
- Use this skill when adding or updating root or nested `AGENTS.md` files.
- Use this skill before accepting AGENTS policy changes.
- Do not use this skill for user/project instruction validation.

## Required Inputs
- Target `AGENTS.md` path.
- Repository path context for link/path validation.
- Policy expectations for session-state and command namespace.

## Workflow
1. Run validation phases from `references/phase-checks.md`.
2. Generate report using `references/report-contract.md`.
3. Apply deterministic scoring from `references/scoring.md`.
4. Classify findings into critical/warning/enhancement buckets.
5. Provide concrete fixes for operational contract gaps.

## Output Expectations
- Structured markdown report with five validation phases.
- Compliance score and pass band.
- Explicit list of critical issues, warnings, and enhancements.
- Example fixes for common structural and policy failures.
- Report schema follows `references/report-contract.md`.
- Scoring and grade bands follow `references/scoring.md`.

## Resources
- Phase checks: `references/phase-checks.md`
- Report contract: `references/report-contract.md`
- Scoring model: `references/scoring.md`
- Example target: `../../AGENTS.md`

## Constraints And Safety
- Keep findings deterministic and repository-specific.
- Avoid over-prescriptive style-only feedback.
- Preserve provider-neutral language.
- Do not duplicate full normative specs when suggesting fixes.
