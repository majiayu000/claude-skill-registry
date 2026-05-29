---
name: feature-spec-orchestrator
description: Create feature spec files from project docs, commit and push to main, and create matching feature branches from main.
trigger: always_on
---
This skill follows `engineering-doctrine` and `structured-workflow`.

## When To Use
- When a user asks for new feature specs in `docs/dev/orchestration/`.
- When the workflow requires aligning specs to feature branches.

## Inputs
- Project docs in `docs/dev/orchestration/` (especially `project_context.md`, `project_design_spec.md`, `project_manifesto.md`).
- Spec template `docs/dev/orchestration/template_tech_spec.md`.

## Required Outputs
- One spec file per feature in `docs/dev/orchestration/`.
- Filename must include the exact feature branch name.
- Specs must be implementation-ready and traceable to project docs.

## Execution Workflow
1. **Clarify**
   - Confirm features or choose an appropriate set from the project roadmap if asked to decide.
   - Decide on a branch naming scheme (e.g., `feat-...`) and use it consistently.
2. **Decide**
   - Map each feature to a scoped spec aligned with the roadmap milestones and constraints.
   - Use the template sections; expand with additional sections if required by project conventions.
3. **Execute**
   - Create spec files in `docs/dev/orchestration/` with filenames like:
     - `feature-spec__<branch-name>.md`
   - Populate each spec using `template_tech_spec.md` plus any required sections from agent guidance.
4. **Verify**
   - Ensure each spec references relevant project context and has testable requirements.
   - Confirm filenames include the branch name verbatim.
5. **Sync (Git)**
   - Commit specs to `main` with a clear message.
   - Push `main` to `origin` before creating any feature branches.
   - Create feature branches from updated `main` with the same names used in the spec filenames.
   - Push all new feature branches to `origin`.

## Guardrails
- Do not include unrelated files (e.g., logs, test outputs) in commits.
- Do not alter existing specs unless explicitly requested.
- Keep content deterministic and avoid speculative scope beyond the docs.

