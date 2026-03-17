---
name: "create-project-instructions"
description: "Create project-context AGENTS.md files using phased discovery, required operational sections, and session-state modeling."
metadata:
  source_prompt: "prompts/create-project-instructions.prompt.md"
  workflow_type: "generation"
---

# Create Project Context AGENTS

## Purpose
Generate project-context `AGENTS.md` files with required sections, role definitions, command namespace controls, and validation-ready structure.

## When To Use
- Use this skill when the task is to create or regenerate project-context `AGENTS.md`.
- Use this skill when project context must include role/phase/style defaults.
- Do not use this skill for user-context instruction generation.

## Required Inputs
- Project name, description, and current phase.
- Tech stack, architecture, and repository structure.
- Roles, default session state, and command namespace.
- Objectives, testing strategy, and documentation standards.

## Workflow
1. Run phased discovery using `references/discovery-phases.md`.
2. Apply required output schema from `references/output-schema.md`.
3. Build command and role structures using:
   - `references/command-template.md`
   - `references/role-template.md`
4. Apply artifact/summary contract from `references/output-format.md`.
5. Validate completeness using `references/quality-checklist.md` before final output.

## Output Expectations
- One complete `AGENTS.md` file with all required project-context sections.
- Session-state and command-reference elements are fully populated.
- Core project-context required-section completeness is enforced through AGENTS structure.
- Role definitions and examples are project-specific and actionable.
- Output remains provider-neutral.
- Output contract and summary format follow `references/output-format.md`.

## Resources
- Discovery workflow: `references/discovery-phases.md`
- Output schema: `references/output-schema.md`
- Command template: `references/command-template.md`
- Role templates: `references/role-template.md`
- Output contract: `references/output-format.md`
- Quality checklist: `references/quality-checklist.md`
- Structure baseline: `../../templates/AGENTS_template.md`
- Example reference: `../../AGENTS.md`

## Constraints And Safety
- Keep recommendations tied to project scope.
- Avoid placeholders in final command examples unless explicitly unresolved.
- Use relative paths for references.
- Do not introduce provider-specific assumptions.
