---
name: "create-agents-md"
description: "Create concise, repository-specific AGENTS.md files with operational contract, precedence rules, and drift-control guidance."
metadata:
  source_prompt: "prompts/create-agents-md.prompt.md"
  workflow_type: "generation"
---

# Create AGENTS.md

## Purpose
Generate a complete root `AGENTS.md` file that acts as an operational entrypoint while preserving source-of-truth and repository governance rules.

## When To Use
- Use this skill when adding or refreshing repository `AGENTS.md`.
- Use this skill when repository map, precedence, and session controls must be documented concisely.
- Do not use this skill for project/user instruction file generation.

## Required Inputs
- Repository purpose and canonical paths.
- Source precedence and key references.
- Session-state defaults and command namespace rules.
- Drift-control requirements.

## Workflow
1. Run seven-phase discovery using `references/discovery-phases.md`.
2. Apply required element contract from `references/required-elements.md`.
3. Generate artifact using `references/output-format.md`.
4. Validate result against `references/quality-checklist.md`.
5. Ensure links/paths remain relative and repository-accurate.

## Output Expectations
- One complete root `AGENTS.md` file.
- Includes purpose, precedence, repo map, command policy, and drift-control.
- Uses provider-neutral wording and valid relative links.
- Remains scannable and operationally actionable.
- Output contract and summary format follow `references/output-format.md`.

## Resources
- Discovery workflow: `references/discovery-phases.md`
- Required element contract: `references/required-elements.md`
- Output contract: `references/output-format.md`
- Quality checklist: `references/quality-checklist.md`
- Canonical template: `../../templates/AGENTS_template.md`
- Repository example: `../../AGENTS.md`

## Constraints And Safety
- Do not duplicate full normative specs in AGENTS.
- Preserve canonical path stability.
- Keep guidance deterministic and testable.
- Use relative path references only.
