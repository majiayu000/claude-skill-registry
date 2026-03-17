---
name: "create-skill"
description: "Create canonical SKILL.md artifacts with deterministic schema, workflow, safety, and quality checks."
metadata:
  source_prompt: "prompts/create-skill.prompt.md"
  workflow_type: "generation"
---

# Create Skill

## Purpose
Generate complete `SKILL.md` artifacts for one skill folder, with explicit constraints and reusable references.

## When To Use
- Use this skill when creating a new skill folder under `skills/`.
- Use this skill when regenerating a `SKILL.md` file to align with repository skill standards.
- Do not use this skill for validating an existing skill.

## Required Inputs
- Skill slug (`name`) and target folder path.
- Capability summary and usage triggers.
- Required inputs, workflow outputs, and failure boundaries.
- Safety and portability constraints.

## Workflow
1. Run discovery sequence in `references/discovery-phases.md`.
2. Apply schema and field rules from `references/field-constraints.md`.
3. Assemble required body sections using `references/output-schema.md`.
4. Apply safety constraints from `references/safety.md`.
5. Produce final artifact using `references/output-format.md`.
6. Validate against `references/quality-checklist.md` before final output.

## Output Expectations
- One complete `SKILL.md` artifact at `skills/{name}/SKILL.md`.
- Frontmatter and folder-name parity are correct.
- Body sections are complete, actionable, and concise.
- Output remains provider-neutral and portable.

## Resources
- Discovery workflow: `references/discovery-phases.md`
- Field constraints: `references/field-constraints.md`
- Output schema: `references/output-schema.md`
- Safety policy: `references/safety.md`
- Output contract: `references/output-format.md`
- Quality checklist: `references/quality-checklist.md`
- Skill template: `../../templates/skill_template/SKILL.md`

## Constraints And Safety
- Keep skill instructions concise and execution-oriented.
- Avoid provider-specific lock-in wording.
- Use relative paths for local references.
- Treat `allowed-tools` as optional/experimental unless explicitly required.
