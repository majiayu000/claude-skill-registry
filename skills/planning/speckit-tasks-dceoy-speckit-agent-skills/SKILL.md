---
name: speckit-tasks
description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
allowed-tools: Bash, Read, Write, Grep, Glob
handoffs:
  - label: Analyze For Consistency
    agent: speckit.analyze
    prompt: Run a project analysis for consistency
    send: true
  - label: Implement Project
    agent: speckit.implement
    prompt: Start the implementation in phases
    send: true
---

# Spec-Kit Tasks

Generate actionable, dependency-ordered tasks from design artifacts. Third step in spec-kit workflow.

## When to Use

- After creating plan.md with `speckit-plan`
- Ready to break down implementation into tasks
- Need to estimate and organize work

## Execution Workflow

1. **Setup**: Run `.specify/scripts/bash/check-prerequisites.sh --json` to get FEATURE_DIR and AVAILABLE_DOCS
2. **Load design documents**:
   - **Required**: plan.md (tech stack, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md, contracts/, research.md, quickstart.md
3. **Execute task generation workflow**:
   - Extract tech stack, libraries, project structure from plan.md
   - Extract user stories with priorities (P1, P2, P3) from spec.md
   - Map entities (from data-model.md) and endpoints (from contracts/) to user stories
   - Generate tasks organized by user story in priority order
   - Create dependency graph showing user story completion order
   - Mark parallel execution opportunities with `[P]`
   - Validate task completeness (each user story independently testable)
4. **Generate tasks.md** using `.specify/templates/tasks-template.md` structure:
   - Phase 1: Setup (project initialization)
   - Phase 2: Foundational (blocking prerequisites)
   - Phase 3+: One phase per user story (in priority order)
   - Final Phase: Polish & cross-cutting concerns
   - Each task: `- [ ] [TaskID] [P?] [Story?] Description with file path`
5. **Report**: Output path, total task count, task count per user story, parallel opportunities, suggested MVP scope

## Key Points

- **STRICT task format** (REQUIRED): `- [ ] [TaskID] [P?] [Story?] Description with file path`
  - ✅ Checkbox required: `- [ ]` (not `- ` or `*`)
  - ✅ Task ID: Sequential (T001, T002, T003...) in execution order
  - ✅ `[P]` marker: ONLY if parallelizable (different files, no dependencies)
  - ✅ `[Story]` label: REQUIRED for user story phases ([US1], [US2], etc.) - NOT for Setup/Foundation/Polish
  - ✅ Description MUST include exact file path
  - Examples:
    - `- [ ] T001 Create project structure per implementation plan` (Setup - no story label)
    - `- [ ] T012 [P] [US1] Create User model in src/models/user.py` (User story task, parallelizable)
- **Tests are OPTIONAL**: Only generate test tasks if explicitly requested in spec or user asks for TDD
- **Organization by user story** enables independent implementation and testing
- Each user story phase should be complete and independently testable
- Map all components to their story (models, services, endpoints, tests)
- Break into small, focused tasks (2-8 hours each)
- Mark parallelizable tasks (different files, no dependencies)

## Next Steps

After creating tasks.md:

- **Analyze** for consistency with `speckit-analyze` (optional)
- **Start implementation** with `speckit-implement`
- **Convert to issues** with `speckit-taskstoissues` (optional)

## See Also

- `speckit-plan` - Create technical implementation strategy
- `speckit-analyze` - Validate cross-artifact consistency
- `speckit-implement` - Execute implementation plan
- `speckit-taskstoissues` - Convert tasks to GitHub issues
