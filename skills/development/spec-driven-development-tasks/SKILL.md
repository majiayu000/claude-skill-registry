---
name: spec_driven_development.tasks
description: "Converts the implementation plan into actionable, ordered development tasks. Use after plan is validated."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **User Story Organization**: Are tasks organized by user story?
            2. **Dependencies Sequenced**: Are task dependencies correctly ordered?
            3. **Parallel Tasks Marked**: Are parallelizable tasks identified with [P] markers?
            4. **File Paths Specified**: Does each task specify which files it creates/modifies?
            5. **TDD Structure**: Are test tasks included before or alongside implementation tasks?
            6. **Checkpoints Defined**: Are validation checkpoints included between phases?
            7. **Granularity Appropriate**: Are tasks small enough to be completed in one session?
            8. **File Created**: Has tasks.md been created in `specs/[feature-name]/`?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response AND
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met OR the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
  SubagentStop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **User Story Organization**: Are tasks organized by user story?
            2. **Dependencies Sequenced**: Are task dependencies correctly ordered?
            3. **Parallel Tasks Marked**: Are parallelizable tasks identified with [P] markers?
            4. **File Paths Specified**: Does each task specify which files it creates/modifies?
            5. **TDD Structure**: Are test tasks included before or alongside implementation tasks?
            6. **Checkpoints Defined**: Are validation checkpoints included between phases?
            7. **Granularity Appropriate**: Are tasks small enough to be completed in one session?
            8. **File Created**: Has tasks.md been created in `specs/[feature-name]/`?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response AND
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met OR the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
---

# spec_driven_development.tasks

**Step 5/6** in **spec_driven_development** workflow

> Spec-driven development workflow that turns specifications into working implementations through structured planning.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/spec_driven_development.plan`
- `/spec_driven_development.clarify`

## Instructions

**Goal**: Converts the implementation plan into actionable, ordered development tasks. Use after plan is validated.

# Generate Task Breakdown

## Objective

Convert the implementation plan into an ordered list of actionable development tasks. Each task should be small enough to complete in a single coding session and clearly specify what files will be created or modified.

## Task

Analyze the implementation plan and specification to generate a comprehensive task list organized by user story with proper dependency ordering.

**Critical**: This step produces a task breakdown, NOT implementation code. Task descriptions should specify:

- What files to create or modify
- What the file should accomplish
- Acceptance criteria for the task

Do NOT include:

- Actual code snippets or implementations
- "Here's how to implement this" examples
- Starter code or templates with real logic

The implement step is where code gets written. This step only plans the work.

### Prerequisites

Before starting, verify these files exist and read them:

1. `specs/[feature-name]/spec.md` - User stories and acceptance criteria
2. `specs/[feature-name]/plan.md` - Architecture and implementation strategy
3. `[docs_folder]/architecture.md` - Project architecture document

If any are missing, inform the user which step they need to complete first.

### Step 1: Identify the Feature

Ask the user which feature to generate tasks for:

```
Which feature would you like to generate tasks for?
```

Verify the plan exists and review it along with the specification.

### Step 2: Analyze Dependencies

Map out the dependency graph:

1. **Infrastructure Dependencies**
   - Database setup must come before data access code
   - Authentication must come before protected routes
   - Base components before compound components

2. **User Story Dependencies**
   - Some stories may depend on others
   - Identify the critical path

3. **Testing Dependencies**
   - Tests often written alongside or before implementation (TDD)
   - Integration tests after unit tests

### Step 3: Task Decomposition

For each user story, break down into tasks:

1. **Database/Model Tasks**
   - Create migrations
   - Define models/entities
   - Add indexes

2. **Backend Tasks**
   - Implement API endpoints
   - Add business logic
   - Integrate services

3. **Frontend Tasks** (if applicable)
   - Create components
   - Add pages/routes
   - Implement state management

4. **Testing Tasks**
   - Unit tests for business logic
   - Integration tests for APIs
   - E2E tests for critical flows

5. **Infrastructure Tasks**
   - Configuration
   - Deployment scripts
   - Monitoring setup

### Step 4: Task Format

Each task should follow this format:

```markdown
### Task [N]: [Descriptive Title]

**User Story**: US-[N] (or "Infrastructure" if not tied to a story)
**Type**: [Database | Backend | Frontend | Test | Infrastructure]
**Dependencies**: [List of task numbers that must complete first, or "None"]
**Parallel**: [P] (add if can run in parallel with other tasks)

**Description:**
[What needs to be done]

**Files to Create/Modify:**

- `path/to/file.ts` - [What to do with this file]
- `path/to/another.ts` - [What to do with this file]

**Acceptance Criteria:**

- [ ] [Specific criterion]
- [ ] [Specific criterion]

**Validation:**
[How to verify this task is complete - e.g., "Run tests", "Check endpoint responds"]
```

### Step 5: Identify Parallel Tasks

Mark tasks that can run in parallel with `[P]`:

- Tasks with no dependencies on each other
- Tasks working on different subsystems
- Independent test suites

**Parallel notation:**

```markdown
### Task 5: Create User Model [P]

### Task 6: Create OAuth Connection Model [P]

(Tasks 5 and 6 can run in parallel after Task 4 completes)
```

### Step 6: Add Checkpoints

Insert validation checkpoints between phases:

```markdown
## Checkpoint: Database Layer Complete

**Verify before proceeding:**

- [ ] All migrations run successfully
- [ ] Models are defined with correct relationships
- [ ] Database can be seeded with test data

**Run:** `npm run db:migrate && npm run db:seed`
```

### Step 7: Create Tasks File

Create `specs/[feature-name]/tasks.md`:

```markdown
# [Feature Name] Implementation Tasks

## Overview

**Total Tasks**: [N]
**Estimated Phases**: [N]
**Parallelizable Tasks**: [N]

## Task Dependency Graph
```

[1] → [2] → [5]
↘
[3] → [4] → [6] → [7]
↗
[1] → [8]

```

## Phase 1: Infrastructure & Database

### Task 1: Setup Database Migrations

**User Story**: Infrastructure
**Type**: Database
**Dependencies**: None

**Description:**
Create the initial database migrations for [entity] tables.

**Files to Create/Modify:**
- `migrations/001_create_users.sql` - Create users table
- `migrations/002_create_oauth_connections.sql` - Create OAuth table

**Acceptance Criteria:**
- [ ] Migrations run without errors
- [ ] Tables created with correct schema
- [ ] Indexes are in place

**Validation:**
Run `npm run db:migrate` and verify tables exist.

---

### Task 2: [Next Task]
...

---

## Checkpoint: Database Layer Complete
[Checkpoint content]

---

## Phase 2: Backend API

### Task 3: [Backend Task]
...

---

## Checkpoint: API Layer Complete
[Checkpoint content]

---

## Phase 3: Frontend Components

### Task 4: [Frontend Task]
...

---

## Checkpoint: Feature Complete
[Final validation checklist]

---

## Summary

| Phase | Tasks | Parallel |
|-------|-------|----------|
| 1. Infrastructure | 1-2 | 0 |
| 2. Backend | 3-6 | 2 |
| 3. Frontend | 7-10 | 3 |
| 4. Testing | 11-14 | 4 |

**Critical Path**: Tasks 1 → 3 → 7 → 11 → 14

**Total Parallelizable**: [N] tasks can run concurrently
```

## Example Dialog

```
Claude: I'll generate implementation tasks. Which feature are you working on?

User: user-authentication

Claude: Let me review the plan and specification...

[Reads specs/user-authentication/plan.md and spec.md]

Based on the plan, I see we need:
- Database: Users and OAuth connections tables
- API: Signup, login, OAuth, and verification endpoints
- Frontend: Signup form, login form, OAuth buttons

I'll organize tasks by user story and phase. Here's the structure:

**Phase 1: Database (4 tasks)**
- Task 1: Create users migration
- Task 2: Create OAuth connections migration [P]
- Task 3: Create user model
- Task 4: Create OAuth connection model [P]

**Phase 2: Authentication Backend (6 tasks)**
- Task 5: Implement password hashing utility
- Task 6: Implement JWT token service [P]
- Task 7: Create signup endpoint
- Task 8: Create login endpoint [P]
- Task 9: Create OAuth callback handler
- Task 10: Create email verification endpoint

**Phase 3: Frontend (4 tasks)**
- Task 11: Create signup form component
- Task 12: Create login form component [P]
- Task 13: Create OAuth button component [P]
- Task 14: Add authentication pages

**Phase 4: Testing (4 tasks)**
- Task 15: Unit tests for auth utilities
- Task 16: Integration tests for auth API [P]
- Task 17: E2E test for signup flow [P]
- Task 18: E2E test for login flow [P]

That's 18 tasks total, with 9 parallelizable.

Does this breakdown look right? Any tasks you'd like to add or modify?

User: Looks good!

Claude: Creating the tasks file...

✓ Task breakdown created!

**File created:**
- specs/user-authentication/tasks.md

**Summary:**
- 18 tasks across 4 phases
- 9 tasks can run in parallel
- Critical path: 9 tasks in sequence
- 4 checkpoints for validation

**Next step:**
Run `/spec_driven_development.implement` to start executing tasks.
```

## Task Sizing Guidelines

**Good task size:**

- Can be completed in 15-60 minutes
- Creates/modifies 1-3 files
- Has clear start and end state
- Can be validated independently

**Too large (split it):**

- Takes more than 2 hours
- Touches more than 5 files
- Has multiple distinct outcomes
- Hard to validate incrementally

**Too small (combine it):**

- Takes less than 5 minutes
- Is just configuration
- Can't be validated alone

## Output Format

### specs/[feature-name]/tasks.md

A markdown document containing:

- Task dependency overview/graph
- Numbered tasks organized by phase
- Each task with full details (story, type, dependencies, files, criteria)
- Checkpoints between phases
- Summary table with parallelization info

**Location**: `specs/[feature-name]/tasks.md`

After creating the file:

1. Summarize total tasks and phases
2. Highlight parallelization opportunities
3. Show the critical path
4. Tell the user to run `/spec_driven_development.implement` to begin implementation

## Quality Criteria

- Tasks are organized by user story
- Dependencies are correctly sequenced
- Parallel tasks are identified with [P]
- Each task specifies files to create/modify
- Tasks are appropriately sized
- Checkpoints exist between phases
- Testing tasks are included
- Critical path is identifiable
- File created in correct location
- **No implementation code**: Tasks describe what to build, not how to code it



## Required Inputs


**Files from Previous Steps** - Read these first:
- `specs/[feature-name]/plan.md` (from `plan`)
- `specs/[feature-name]/spec.md` (from `clarify`)
- `[docs_folder]/architecture.md` (from `plan`)

## Work Branch

Use branch format: `deepwork/spec_driven_development-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/spec_driven_development-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `specs/[feature-name]/tasks.md`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

Stop hooks will automatically validate your work. The loop continues until all criteria pass.

**Criteria (all must be satisfied)**:
1. **User Story Organization**: Are tasks organized by user story?
2. **Dependencies Sequenced**: Are task dependencies correctly ordered?
3. **Parallel Tasks Marked**: Are parallelizable tasks identified with [P] markers?
4. **File Paths Specified**: Does each task specify which files it creates/modifies?
5. **TDD Structure**: Are test tasks included before or alongside implementation tasks?
6. **Checkpoints Defined**: Are validation checkpoints included between phases?
7. **Granularity Appropriate**: Are tasks small enough to be completed in one session?
8. **File Created**: Has tasks.md been created in `specs/[feature-name]/`?


**To complete**: Include `<promise>✓ Quality Criteria Met</promise>` in your final response only after verifying ALL criteria are satisfied.

## On Completion

1. Verify outputs are created
2. Inform user: "Step 5/6 complete, outputs: specs/[feature-name]/tasks.md"
3. **Continue workflow**: Use Skill tool to invoke `/spec_driven_development.implement`

---

**Reference files**: `.deepwork/jobs/spec_driven_development/job.yml`, `.deepwork/jobs/spec_driven_development/steps/tasks.md`