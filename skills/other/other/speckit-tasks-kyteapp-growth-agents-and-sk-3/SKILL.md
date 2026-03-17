---
name: speckit-tasks
description: Generate actionable, dependency-ordered tasks.md for the feature based on available design artifacts
---

# Speckit-Tasks: Task Breakdown Generation

## Purpose

Generate actionable, dependency-ordered task breakdown organized by user story, enabling independent implementation and testing of feature increments.

## Prerequisites

- Completed specification (`spec.md` exists)
- Completed technical plan (`plan.md` exists)
- Optional: `data-model.md`, `contracts/`, `research.md`, `quickstart.md`

## What This Skill Does

1. Loads specification and plan
2. Maps requirements to tasks
3. Organizes tasks by user story (from spec)
4. Identifies dependencies and parallel opportunities
5. Creates execution phases (Setup → Foundation → User Stories → Polish)
6. Generates task checklist with file paths

## Key Principles

### Organize by User Story
- Each user story (P1, P2, P3...) gets its own phase
- Map all components to their story (models, services, endpoints, tests)
- Enable independent implementation of each story
- Each story is a complete, testable vertical slice

### Every Task Has File Path
- Specific, not vague: `src/models/user.py` not "user file"
- Exact location: Full path from project root
- Clear deliverable: One task = One file or component

### Dependencies Explicit
- Sequential tasks: Run in order
- Parallel tasks: Marked with [P] - can run simultaneously
- Story dependencies: Most stories should be independent
- Foundation first: Shared infrastructure before stories

### Independently Testable Stories
- Each story has clear test criteria
- Complete vertical slice (model → service → endpoint)
- Can be verified without other stories
- Enables MVP and incremental delivery

## Template Location

**IMPORTANT:** The tasks template is located at:
`.github/skills/speckit-tasks/tasks-template.md`

This template MUST be loaded and used as the base structure for all task breakdown generation.

## Execution Flow

All execution logic is now contained within this skill. The skill handles:
- Prerequisites checking
- Design document loading
- Task generation by user story
- Dependency mapping

### Quick Summary

1. **Setup:** Run `check-prerequisites.sh` to get feature paths
2. **Load template** from `.github/skills/speckit-tasks/tasks-template.md`
3. **Load design docs:**
   - Required: `plan.md` (tech stack), `spec.md` (user stories)
   - Optional: `data-model.md`, `contracts/`, `research.md`, `quickstart.md`
4. **Execute task generation:**
   - Extract tech stack and project structure from plan
   - Extract user stories with priorities from spec
   - Map entities to stories (from data-model)
   - Map endpoints to stories (from contracts)
   - Extract decisions for setup (from research)
   - Generate tasks organized by user story
   - Create dependency graph
   - Identify parallel opportunities
5. **Generate tasks.md** using template structure
6. **Report completion:** Task counts, parallel opportunities, MVP scope

## Task Organization

### Phase Structure

```
Phase 1: Setup
  - Project initialization
  - Dependency installation
  - Configuration
  
Phase 2: Foundation
  - Shared infrastructure
  - Blocking prerequisites for ALL stories
  - Authentication, logging, database connection
  
Phase 3: User Story 1 (P1)
  - [US1] Tests (if requested)
  - [US1] Models
  - [US1] Services
  - [US1] Endpoints/UI
  - [US1] Integration
  
Phase 4: User Story 2 (P2)
  - [US2] Tasks...
  
Phase N: Polish & Cross-Cutting
  - Documentation
  - Performance optimization
  - Error handling polish
```

### Task Format (REQUIRED)

Every task MUST follow this format:

```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Components:**
1. **Checkbox:** `- [ ]` (markdown checkbox)
2. **Task ID:** T001, T002, T003... (sequential)
3. **[P] marker:** Include ONLY if parallelizable
4. **[Story] label:** [US1], [US2], [US3], etc. (REQUIRED for story tasks)
5. **Description:** Clear action with exact file path

**Examples:**

✅ **CORRECT:**
```markdown
- [ ] T001 Create project structure per implementation plan
- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py
- [ ] T012 [P] [US1] Create User model in src/models/user.py
- [ ] T014 [US1] Implement UserService in src/services/user_service.py
```

❌ **WRONG:**
```markdown
- [ ] Create User model (missing ID, Story label, file path)
- [ ] [US1] Create model (missing Task ID, file path)
T001 [US1] Create model (missing checkbox)
```

## Task Generation Rules

### From User Stories (PRIMARY ORGANIZATION)

Map all components to their story:
- Models needed for that story
- Services needed for that story
- Endpoints/UI needed for that story
- Tests specific to that story (if requested)

### From Contracts

- Map each endpoint → user story it serves
- If tests requested: Contract test before implementation
- Include request/response validation

### From Data Model

- Map each entity to story(ies) that need it
- If entity serves multiple stories: Earliest story or Foundation phase
- Relationships → service layer tasks

### From Setup/Infrastructure

- Shared infrastructure → Setup phase (Phase 1)
- Blocking prerequisites → Foundation phase (Phase 2)
- Story-specific setup → within story phase

## Tests Are OPTIONAL

**CRITICAL:** Only generate test tasks if:
- Explicitly requested in specification
- User requests TDD approach
- Feature spec mentions testing requirements

**Default:** No test tasks unless specifically requested

## Success Indicators

Tasks are ready when:
- ✅ All tasks follow checklist format (checkbox, ID, labels, paths)
- ✅ Tasks organized by user story
- ✅ Dependencies clear (sequential vs parallel)
- ✅ Each story independently testable
- ✅ File paths specific and complete
- ✅ Parallel opportunities identified ([P] markers)
- ✅ MVP scope clear (typically User Story 1)

## Output

```
specs/N-feature-name/
└── tasks.md                   # Complete task breakdown

Summary includes:
- Total task count
- Task count per user story
- Parallel opportunities
- Independent test criteria per story
- Suggested MVP scope
- Format validation confirmation
```

## Next Step

After tasks are complete:
- **Option A:** Use `executing-plans` for sequential task execution
- **Option B:** Use `test-driven-development` for TDD approach
- **Option C:** Use `speckit-checklist` to validate requirements quality first

## Common Mistakes

### ❌ Missing File Paths
**Wrong:** `- [ ] T001 [US1] Create User model`
**Right:** `- [ ] T001 [US1] Create User model in src/models/user.py`

### ❌ Missing Story Labels
**Wrong:** `- [ ] T012 Implement authentication` (which story?)
**Right:** `- [ ] T012 [US1] Implement authentication in src/auth/service.py`

### ❌ Vague Tasks
**Wrong:** `- [ ] T001 Setup database`
**Right:** `- [ ] T001 Create database schema in migrations/001_init.sql`

### ❌ Wrong Organization
**Wrong:** All tasks in one phase
**Right:** Organized by user story (Setup → Foundation → US1 → US2 → Polish)

### ❌ Assuming Tests Required
**Wrong:** Generate test tasks for every feature
**Right:** Only generate tests if explicitly requested

### ❌ Incorrect Parallel Markers
**Wrong:** Mark dependent tasks as [P]
**Right:** Only mark truly independent tasks as [P] (different files, no dependencies)

## Related Skills

- **speckit-plan** - Previous step (create technical plan)
- **executing-plans** - Next step option A (sequential execution)
- **test-driven-development** - Next step option B (TDD approach)
- **speckit-checklist** - Generate quality validation checklists
