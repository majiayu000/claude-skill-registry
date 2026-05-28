---
name: si
description: Execute structured TDD implementation following task documents. Use when starting, continuing, or resuming implementation of a task from tasks/ directory. Also handles addressing code review feedback.
argument-hint: [task-directory]
allowed-tools: ["Task", "AskUserQuestion", "Edit", "Read", "Bash", "Glob", "Grep", "Skill", "TodoWrite"]
---

# Start Implementation Command

## PRIMARY OBJECTIVE
Implement features systematically with comprehensive tracking on feature branches.

Three modes of operation:
1. **Start** — Begin implementation from scratch
2. **Continue** — Resume in-progress implementation
3. **Address CR** — Apply code review feedback

Before any work, determine which mode applies by reviewing the task document status and git history.

## CONSTRAINTS
- Follow existing task document in `tasks/` directory
- Git writes require explicit user permission:
  - Do **NOT** create commits, push branches, open PRs, merge, rebase, or otherwise modify git state unless the user explicitly approves it.

## WORKFLOW STEPS

### **STEP 1: Task Validation**

1. **Ask user**: "Which task to implement? Provide task name or path." If it was not provided
   - List tasks in `tasks/` if unclear

2. **Validate document**:
   - Confirm the task exists (either a single `.md` file OR a `tasks/task-YYYY-MM-DD-slug/` directory).
   - Confirm scope is unambiguous:
     - Clear acceptance criteria
     - Clear "done" definition (what must be true for completion)
   - Confirm task status is appropriate (e.g., "Ready for Implementation" vs "Draft") and ask before proceeding if unclear.
   - Confirm Linear issue exists and is referenced (ID/link).
   - Confirm there is an implementation plan (even if small): impacted components + test plan.

### **STEP 2: Setup**
Note: Skip this step when continuing implementation or addressing Code Review Results

#### **Status Updates**
1. **Update task status** to "In Progress" with timestamp
2. **Create feature branch** (name must follow repo convention): `feature/wyt-[ID]-[slug]`
3. **Update task document** with branch name
4. **Permission gate**: If any git operation is required (branch creation, commit, push), ask for explicit approval first.

### **STEP 3: Implementation**

#### **Parallelization (optional)**

If you believe part of the work can be done safely in parallel, use the `parallelization` skill:

- `.claude/skills/parallelization/SKILL.md`

---

#### **Sequential Mode**

#### **Before Each Step:**
1. **Announce**: "Starting Step [N]: [Description]"
2. **Review requirements**: Acceptance criteria, tests, artifacts

#### **During Implementation (TDD Approach):**
1. **Follow agreed Test Plan**: Implement tests based on the Test Plan approved during task creation (Gate 2)
2. **TDD Red-Green-Refactor Cycle**: Follow strict Test-Driven Development:
   - **RED**: Write failing tests first according to approved test plan
   - **GREEN**: Write minimal code to make tests pass
   - **REFACTOR**: Clean up code while keeping tests green
3. **Implement tests by approved categories**:
   - **Business Logic Tests**: As/if defined in approved test plan
   - **State Transition Tests**: As/if defined in approved test plan
   - **Error Handling Tests**: As/if defined in approved test plan
   - **Integration Tests**: As/if defined in approved test plan
   - **User Interaction Tests**: As/if defined in approved test plan
4. **Testing tools**:
   - Prefer silent scripts in AI-agent mode (backend): `npm run test:silent`, `npm run test:unit:silent`, `npm run test:integration:silent`, `npm run test:e2e:silent`
   - Local runs are fine with `npm run test` when you need full output
   - `npm run test:ci` when the Postgres-backed integration suite is required
   - `npm run test:db:start|migrate|stop` scripts to spin up and tear down the Supabase-compatible test DB
5. **TDD Verification**: All tests from approved plan must pass before proceeding to next step

#### **After Each Step:**
1. **Update the task document** (REQUIRED - not just chat output):
   - Mark the step checkbox as complete: `- [ ]` → `- [x]`
   - Add **Changelog** entry describing what was done
   - Update **Tests** field with command run + result
   - If tests are defined in the Test Plan section, mark those checkboxes too
   - **Parallel mode note**: when using parallel workers, workers should not edit shared task docs; apply/merge worker outputs first, then update the task doc once to avoid conflicts.

   Example of updating a step in the task doc:
   ```markdown
   - [x] Sub-step 3.1: Update CreateSessionUseCase logic
     - **Tests**: Test Suite 3 - PASS
     - **Changelog**: Injected WordGroupService, added validateGroupHasSufficientWords() method
   ```

2. **Commit changes (permission gate)**:
   - If the user has **not explicitly approved** git writes: ask for permission **before** any `git` command.
   - If approved and the step is complete: use **conventional commits** (optionally include scope) and include an issue reference when applicable:
     - `git add [files] && git commit -m "feat|fix|refactor: [step summary]" -m "Refs: WYT-123"`

#### **Error Recovery**
- **Tests fail**: Fix the failing code, re-run tests. Do NOT skip or delete failing tests.
- **Quality gate fails**: Read the Quality Gate Report, address each failure, re-run.
- **Task document incomplete**: Ask user to clarify missing criteria before proceeding.

### **STEP 4: Completion**

#### **Final Verification**
1. **Run quality gates via agent**:
   - Use Task tool with subagent_type: "automated-quality-gate"
   - Provide `task_path` (absolute path to `tasks/task-YYYY-MM-DD-slug/`) and current `branch`
   - Agent runs format/lint/types/tests/build and writes a Quality Gate Report in the task directory

#### **Finalize Task Document**
1. **Update status** to "Ready for Review" with timestamp
2. **Verify all checkboxes are accurate**
3. **Add implementation summary**

### **STEP 5: Prepare for Code Review**
1. **Permission gate (required)**:
   - Creating a PR and pushing branches requires **explicit user approval** for git writes.
   - If approval is not given, stop and ask for permission before proceeding.

2. **Validate task documentation**:
   - Use Task tool with subagent_type: "task-pm-validator"
   - Provide the exact task document path (e.g., `tasks/task-2025-01-15-feature-name.md`)

3. **Create PR + sync Linear (single path)**:
   - Use Task tool with subagent_type: "create-pr-agent"
   - Provide the exact task document path (e.g., `tasks/task-2025-01-15-feature-name.md`)
   - This agent handles PR creation and updates the task document with PR links. For Linear updates use the `cc-linear` skill (`.claude/skills/cc-linear/SKILL.md`).
