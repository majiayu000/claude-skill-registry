---
name: "validate-project-instructions"
description: "Validate project-context AGENTS.md files for required sections, session-state model completeness, role quality, and scoring compliance."
metadata:
  source_prompt: "prompts/validate-project-instructions.prompt.md"
  workflow_type: "validation"
---

# Validate Project Context AGENTS

## Purpose
Validate project-context `AGENTS.md` files with deterministic checks for required sections, session-state controls, role definitions, and core required-section completeness.

## When To Use
- Use this skill to validate project-context `AGENTS.md` files.
- Use this skill when reviewing project context quality prior to active use.
- Do not use this skill for user-context instruction validation.

## Required Inputs
- Target project-context `AGENTS.md` path.
- Expected section model and command reference expectations.
- Any strictness preferences for warnings vs required fixes.

## Workflow
1. Run validation phases from `references/phase-checks.md`.
2. Generate report using `references/report-contract.md`.
3. Apply deterministic scoring from `references/scoring.md`.
4. Classify findings into critical/warning/enhancement buckets.
5. Produce project-specific remediation guidance.

## Output Expectations
- Structured markdown report with five validation phases.
- Clear status for critical issues vs warnings.
- Numeric score and grading band.
- Concrete example fixes for major gaps.
- Report schema follows `references/report-contract.md`.
- Scoring and grade bands follow `references/scoring.md`.

## Resources
- Phase checks: `references/phase-checks.md`
- Report contract: `references/report-contract.md`
- Scoring model: `references/scoring.md`
- Example target: `../../AGENTS.md`

## Constraints And Safety
- Keep findings specific and actionable.
- Preserve project terminology when proposing fixes.
- Keep validation language provider-neutral.
- Do not rewrite source files automatically.
