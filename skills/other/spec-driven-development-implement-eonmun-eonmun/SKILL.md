---
name: spec_driven_development.implement
description: "Generates code and assets by executing the task breakdown. Use when ready to build the feature."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **Prerequisites Met**: Were all spec/plan/tasks artifacts validated before starting?
            2. **Task Order Followed**: Were tasks executed in dependency order?
            3. **Tests Written**: Are tests created alongside or before implementation?
            4. **Acceptance Criteria Met**: Does the implementation satisfy all acceptance criteria from spec?
            5. **Code Quality**: Does the code meet the standards defined in the constitution?
            6. **Progress Tracked**: Was progress communicated throughout implementation?
            7. **All Tasks Complete**: Have all tasks in tasks.md been completed?

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

            1. **Prerequisites Met**: Were all spec/plan/tasks artifacts validated before starting?
            2. **Task Order Followed**: Were tasks executed in dependency order?
            3. **Tests Written**: Are tests created alongside or before implementation?
            4. **Acceptance Criteria Met**: Does the implementation satisfy all acceptance criteria from spec?
            5. **Code Quality**: Does the code meet the standards defined in the constitution?
            6. **Progress Tracked**: Was progress communicated throughout implementation?
            7. **All Tasks Complete**: Have all tasks in tasks.md been completed?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response AND
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met OR the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
---

# spec_driven_development.implement

**Step 6/6** in **spec_driven_development** workflow

> Spec-driven development workflow that turns specifications into working implementations through structured planning.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/spec_driven_development.tasks`
- `/spec_driven_development.plan`
- `/spec_driven_development.clarify`

## Instructions

**Goal**: Generates code and assets by executing the task breakdown. Use when ready to build the feature.

# Execute Implementation

## Objective

Execute the task breakdown to generate working code that implements the feature specification. Tasks are executed in dependency order, with progress tracked throughout.

## Task

Systematically work through each task in `tasks.md`, implementing the feature according to the specification and plan.

### Prerequisites

Before starting, verify ALL prerequisite files exist:

1. `[docs_folder]/constitution.md` - Project principles
2. `[docs_folder]/architecture.md` - Project architecture document
3. `specs/[feature-name]/spec.md` - Requirements and acceptance criteria
4. `specs/[feature-name]/plan.md` - Architecture and technology choices
5. `specs/[feature-name]/tasks.md` - Task breakdown

**If any file is missing**, inform the user which step they need to complete first. Do NOT proceed without all artifacts.

### Step 1: Identify the Feature

Ask the user which feature to implement:

```
Which feature would you like to implement?
```

Load and review all specification artifacts.

### Step 2: Validate Prerequisites

Before implementing, verify:

1. **Specification is complete**
   - All user stories have acceptance criteria
   - No open questions remain
   - Scope is clearly defined

2. **Plan is actionable**
   - Architecture is defined
   - Technology choices are made
   - Data model is specified

3. **Tasks are ready**
   - Tasks are properly sequenced
   - Dependencies are clear
   - Checkpoints are defined

If validation fails, inform the user what needs to be addressed.

### Step 3: Setup Progress Tracking

Create or update progress tracking in tasks.md:

```markdown
## Implementation Progress

**Started**: [Date/Time]
**Current Phase**: 1 of 4
**Tasks Completed**: 0 of 18

| Task | Status     | Notes |
| ---- | ---------- | ----- |
| 1    | ⏳ Pending |       |
| 2    | ⏳ Pending |       |

...
```

**Status indicators:**

- ⏳ Pending
- 🔄 In Progress
- ✅ Complete
- ⚠️ Blocked
- ❌ Failed

### Step 4: Execute Tasks

For each task in order:

1. **Announce the task:**

   ```
   Starting Task [N]: [Title]
   Type: [Type]
   Dependencies: [Met/Pending]
   ```

2. **Verify dependencies are met:**
   - Check all prerequisite tasks are complete
   - If not, skip and note as blocked

3. **Implement the task:**
   - Follow the task description
   - Create/modify specified files
   - Use constitution guidelines for code quality

4. **Validate completion:**
   - Check all acceptance criteria
   - Run specified validation commands
   - Fix any issues before proceeding

5. **Update progress:**
   ```
   ✅ Task [N] Complete
   Files created/modified:
   - path/to/file.ts
   - path/to/another.ts
   ```

### Step 5: Handle Checkpoints

At each checkpoint:

1. **Stop and validate:**

   ```
   📍 Checkpoint: [Name]

   Validating:
   - [ ] [Criterion 1]
   - [ ] [Criterion 2]
   ```

2. **Run validation commands:**
   - Execute tests
   - Run linting
   - Check build

3. **Report status:**

   ```
   Checkpoint [Name]: ✅ PASSED
   All criteria met. Proceeding to Phase [N].
   ```

   OR

   ```
   Checkpoint [Name]: ❌ FAILED
   Issues found:
   - [Issue 1]
   - [Issue 2]

   Addressing issues before proceeding...
   ```

4. **Do not proceed until checkpoint passes**

### Step 6: Handle Parallel Tasks

When encountering parallel tasks:

1. **Identify the parallel group:**

   ```
   Tasks 5 and 6 can run in parallel.
   Implementing Task 5...
   ```

2. **Complete all parallel tasks before moving to dependents:**

   ```
   ✅ Task 5 Complete
   ✅ Task 6 Complete

   Both parallel tasks complete. Proceeding to Task 7.
   ```

### Step 7: Handle Issues

When problems occur:

1. **Document the issue:**

   ```
   ⚠️ Issue in Task [N]:
   [Description of the problem]
   ```

2. **Attempt resolution:**
   - If fixable, fix it
   - If needs clarification, ask user
   - If blocked by external factor, mark as blocked

3. **Update task status:**

   ```markdown
   | 7 | ⚠️ Blocked | Waiting for API credentials |
   ```

4. **Continue with non-dependent tasks:**
   - Skip blocked tasks
   - Proceed with independent tasks
   - Return to blocked tasks when resolved

### Step 8: Verify Acceptance Criteria

After all tasks complete:

1. **Review specification acceptance criteria:**
   - Go through each user story
   - Verify all criteria are met
   - Document any gaps

2. **Run full test suite:**

   ```bash
   npm test
   npm run lint
   npm run build
   ```

3. **Final validation:**

   ```
   ## Implementation Complete

   **Acceptance Criteria Verification:**

   US-1: [Story Title]
   - [x] [Criterion 1] - Implemented in src/auth/signup.ts
   - [x] [Criterion 2] - Tested in tests/auth/signup.test.ts

   US-2: [Story Title]
   - [x] [Criterion 1] - Implemented in src/auth/login.ts
   ...
   ```

### Step 9: Final Report

Produce a completion report:

```markdown
## Implementation Summary

**Feature**: [Feature Name]
**Completed**: [Date/Time]

### Statistics

- Total Tasks: [N]
- Completed: [N]
- Blocked: [N]
- Duration: [Time]

### Files Created

- `src/auth/signup.ts` - Signup endpoint
- `src/auth/login.ts` - Login endpoint
  ...

### Files Modified

- `src/routes/index.ts` - Added auth routes
  ...

### Tests Added

- `tests/auth/signup.test.ts` - 8 tests
- `tests/auth/login.test.ts` - 6 tests
  ...

### Acceptance Criteria Status

- US-1: ✅ All criteria met
- US-2: ✅ All criteria met
- US-3: ⚠️ 1 criterion deferred (noted in spec)

### Notes

[Any important observations or follow-up items]
```

## Example Dialog

```
Claude: I'll implement the feature. Which one are you working on?

User: user-authentication

Claude: Let me verify all prerequisites...

✅ Constitution exists
✅ Specification complete (5 user stories, all clarified)
✅ Plan complete (architecture, data model, API spec)
✅ Tasks complete (18 tasks across 4 phases)

Starting implementation...

---

**Phase 1: Database**

Starting Task 1: Create users migration
Type: Database
Dependencies: None

Creating migration file...

[Creates migrations/001_create_users.sql]

Running migration validation...

✅ Task 1 Complete
Files created:
- migrations/001_create_users.sql

---

Starting Task 2: Create OAuth connections migration [P]
Type: Database
Dependencies: Task 1

[Creates migrations/002_create_oauth_connections.sql]

✅ Task 2 Complete

---

📍 Checkpoint: Database Layer Complete

Validating:
- [x] All migrations run successfully
- [x] Tables created with correct schema
- [x] Indexes are in place

Running: `npm run db:migrate`

Checkpoint Database Layer: ✅ PASSED

---

**Phase 2: Backend API**

Starting Task 3: Implement password hashing utility
Type: Backend
Dependencies: None

[Creates src/utils/password.ts]

Running tests...

✅ Task 3 Complete
Files created:
- src/utils/password.ts
- tests/utils/password.test.ts

---

[Continues through all tasks...]

---

## Implementation Complete!

**Statistics:**
- Total Tasks: 18
- Completed: 18
- Blocked: 0

**Acceptance Criteria:**
All 5 user stories have all criteria met.

**Files Created:** 14
**Tests Added:** 24 tests, all passing

The user-authentication feature is ready for review.
```

## Output Format

This step produces working code:

- Source files as specified in tasks
- Test files alongside implementation
- Configuration as needed

Progress is tracked by updating `specs/[feature-name]/tasks.md` with status.

After completion:

1. Summarize what was implemented
2. List all files created/modified
3. Confirm all acceptance criteria are met
4. Note any issues or follow-up items

## Quality Criteria

- All prerequisite artifacts were validated before starting
- Tasks were executed in correct dependency order
- Checkpoints were validated before proceeding
- Code follows constitution guidelines
- Tests were written alongside implementation
- All acceptance criteria from spec are met
- Progress was tracked throughout
- Final report summarizes implementation



## Required Inputs


**Files from Previous Steps** - Read these first:
- `specs/[feature-name]/tasks.md` (from `tasks`)
- `specs/[feature-name]/plan.md` (from `plan`)
- `specs/[feature-name]/spec.md` (from `clarify`)
- `[docs_folder]/architecture.md` (from `plan`)

## Work Branch

Use branch format: `deepwork/spec_driven_development-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/spec_driven_development-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `src/` (directory)
- `tests/` (directory)

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

Stop hooks will automatically validate your work. The loop continues until all criteria pass.

**Criteria (all must be satisfied)**:
1. **Prerequisites Met**: Were all spec/plan/tasks artifacts validated before starting?
2. **Task Order Followed**: Were tasks executed in dependency order?
3. **Tests Written**: Are tests created alongside or before implementation?
4. **Acceptance Criteria Met**: Does the implementation satisfy all acceptance criteria from spec?
5. **Code Quality**: Does the code meet the standards defined in the constitution?
6. **Progress Tracked**: Was progress communicated throughout implementation?
7. **All Tasks Complete**: Have all tasks in tasks.md been completed?


**To complete**: Include `<promise>✓ Quality Criteria Met</promise>` in your final response only after verifying ALL criteria are satisfied.

## On Completion

1. Verify outputs are created
2. Inform user: "Step 6/6 complete, outputs: src/, tests/"
3. **Workflow complete**: All steps finished. Consider creating a PR to merge the work branch.

---

**Reference files**: `.deepwork/jobs/spec_driven_development/job.yml`, `.deepwork/jobs/spec_driven_development/steps/implement.md`