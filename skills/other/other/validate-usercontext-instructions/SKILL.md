---
name: "validate-usercontext-instructions"
description: "Validate user-context instruction files against schema, section completeness, quality checks, and scoring criteria."
metadata:
  source_prompt: "prompts/validate-usercontext-instructions.prompt.md"
  workflow_type: "validation"
---

# Validate User Context Instructions

## Purpose
Validate user-context instruction files and produce deterministic reports with issues, recommendations, and a compliance score.

## When To Use
- Use this skill to validate `*_usercontext.instructions.md` files.
- Use this skill before publishing or reusing a user-context file.
- Do not use this skill for project `AGENTS.md` (project context) files.

## Required Inputs
- Target file path.
- Expected spec version and required sections.
- Validation strictness expectations (if any).

## Workflow
1. Run validation phases from `references/phase-checks.md`.
2. Generate report using `references/report-contract.md`.
3. Apply deterministic scoring from `references/scoring.md`.
4. Classify findings into critical/warning/enhancement buckets.
5. Produce implementation-ready recommendations.

## Output Expectations
- A markdown validation report with phase-by-phase findings.
- Overall PASS/WARN/FAIL state and numeric score.
- Actionable fixes for critical and warning issues.
- Migration guidance when relevant.
- Report schema follows `references/report-contract.md`.
- Scoring and grade bands follow `references/scoring.md`.

## Resources
- Phase checks: `references/phase-checks.md`
- Report contract: `references/report-contract.md`
- Scoring model: `references/scoring.md`
- Example target: `../../usercontexts/sample_usercontext.instructions.md`
- Example report: `../../usercontexts/sample_usercontext.validation.md`

## Constraints And Safety
- Preserve privacy boundaries in findings and examples.
- Keep recommendations implementation-ready and non-ambiguous.
- Use provider-neutral language.
- Do not modify validated source files automatically.
