---
name: Task Generation
description: Generate user-story-organized task lists from implementation plans. Use when plan exists and user is ready for implementation, mentions "create tasks", "break down work", or asks "what tasks are needed" to implement the feature.
degree-of-freedom: low
allowed-tools: Read, Write
---

@.claude/shared-imports/constitution.md
@.claude/shared-imports/master-todo-utils.md
@.claude/templates/tasks.md

# Task Generation

## Workflow Context

**SDD Phase**: Phase 6 (Task Generation - Automatic)
**Command**: `/tasks` (typically auto-invoked by /plan)
**Prerequisites**: `specs/$FEATURE/plan.md` (created by Phase 5)
**Creates**: `specs/$FEATURE/tasks.md` + updates `todos/master-todo.md` with user story subtasks
**Predecessor**: Phase 5 - `/plan` → `plan.md`
**Successor**: Phase 7 - `/audit` (auto) → `audit-report.md`

### Phase Chain
```
Phase 1: /define-product → memory/product.md
Phase 2: /generate-constitution → memory/constitution.md
Phase 3: /feature → specs/$FEATURE/spec.md + todos/master-todo.md entry
Phase 4: /clarify (if needed) → updated spec.md
Phase 5: /plan → plan.md + research.md + data-model.md
Phase 6: /tasks (auto) → tasks.md + todos/master-todo.md subtasks (YOU ARE HERE)
Phase 7: /audit (auto) → audit-report.md
Phase 8: /implement → code + tests + verification
```

**$FEATURE format**: `NNN-feature-name` (e.g., `001-therapy-app`)

### Automatic Invocation

This skill is typically auto-invoked by `/plan` (Phase 5). After tasks.md is created, it automatically triggers `/audit` (Phase 7) to validate consistency.

---

**Purpose**: Transform implementation plans into executable, user-story-organized task breakdowns following Article VII (User-Story-Centric Organization).

**Constitutional Authority**: Article VII (User-Story-Centric Organization), Article III (Test-First Imperative), Article VIII (Parallelization Markers)

---

## Quick Reference

| Phase | Key Activities | Output | Article |
|-------|---------------|--------|---------|
| **1. Load Context** | Validate prerequisites, load spec.md, plan.md, supporting docs | Context loaded | Article IV |
| **2-3. Task Generation** | Organize by user story, generate tests/impl/verification | Task phases | Article VII, III |
| **4. Parallelization** | Mark [P] for tasks that can run simultaneously | [P] markers added | Article VIII |
| **5. Quality Gate** | Automatically invoke /audit for validation | Audit report | Article V |
| **6. Generate tasks.md** | Write using template, report completion | tasks.md | All |

---

## Phase 1: Load Context

### Step 1.1: Validate Prerequisites

PreToolUse hook blocks tasks.md without plan.md, but verify:

```bash
FEATURE=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "${SPECIFY_FEATURE:-}")

if [[ ! -f "specs/$FEATURE/spec.md" ]]; then
    echo "ERROR: Missing specification (Article IV violation)"
    exit 1
fi

if [[ ! -f "specs/$FEATURE/plan.md" ]]; then
    echo "ERROR: Missing implementation plan (Article IV violation)"
    exit 1
fi
```

### Step 1.2: Load Specification (User Stories)

```bash
Read specs/$FEATURE/spec.md
```

**Extract**:
- User stories with priorities (P1, P2, P3...)
- Independent test criteria per story
- Functional requirements

### Step 1.3: Load Implementation Plan (Tech Details)

```bash
Read specs/$FEATURE/plan.md
```

**Extract**:
- Tech stack and frameworks
- Component breakdown
- Acceptance criteria (≥2 per story)
- File structure
- Integration points

### Step 1.4: Load Supporting Documents (If Available)

```bash
Read specs/$FEATURE/data-model.md  # Entity designs
Read specs/$FEATURE/contracts/*.md  # API specifications
Read specs/$FEATURE/quickstart.md  # Test scenarios
```

---

## Phase 2-3: Task Generation Workflow

**See:** @.claude/skills/generate-tasks/workflows/task-generation.md

**Summary**:

**Phase 2: Organize by User Story** (Article VII mandate)
- Required phase structure: Setup → Foundational → User Story Phases → Polish
- One phase per user story (P1, P2, P3...)
- Within each story: Tests → Implementation → Verification

**Phase 3: Generate Tasks**
- Setup tasks: Project initialization, dependencies
- Foundational tasks: Blocking prerequisites for ALL stories
- User Story tasks: Test-first approach (Article III)
  - Tests (≥2 per story)
  - Implementation (models, services, endpoints, UI)
  - Verification (run tests, validate independently)
- Polish tasks: Documentation, cleanup

**Task Format**:
- Task ID: T### (sequential numbering)
- Story Label: [US#] for traceability
- Parallel Marker: [P] for simultaneous execution

---

## Phase 4: Parallelization Marking

**See:** @.claude/skills/generate-tasks/workflows/parallelization.md

**Summary**:

Mark tasks with `[P]` if they meet ALL criteria:
1. **Different files** - No file conflicts with other parallel tasks
2. **No dependencies** - Doesn't depend on incomplete tasks
3. **Independent** - Can run without coordination

**Common Patterns**:
- Test writing (different test files) → Parallel
- Setup tasks (independent config) → Parallel
- Documentation updates (different docs) → Parallel
- Model dependencies (B uses A) → Sequential

**Document** parallel opportunities per phase in summary.

---

## Phase 5: Quality Gate Enforcement

**See:** @.claude/skills/generate-tasks/workflows/quality-gates.md

**Summary**:

After tasks.md created, **automatically invoke /audit command** (Article V requirement).

**DO NOT ask user to run /audit manually** - this is automatic enforcement.

**Audit Validates**:
1. Article IV compliance (spec → plan → tasks sequence)
2. Article VII compliance (user-story-centric organization)
3. Article III compliance (≥2 ACs per story, tests first)
4. Constitution violations (CRITICAL priority)
5. Requirement coverage (100% expected)
6. Ambiguities and underspecification

**On CRITICAL failures**: Implementation BLOCKED, user must fix issues and re-run /tasks
**On successful audit**: Ready for `/implement plan.md`

---

## Phase 6: Generate tasks.md

### Step 6.1: Write Using Template

Use `@.claude/templates/tasks.md` structure:

```yaml
---
feature: <number>-<name>
created: <YYYY-MM-DD>
plan: specs/<number>-<name>/plan.md
status: Ready for Implementation
total_tasks: <count>
---
```

**Include**:
1. **Summary**: Total tasks, story breakdown
2. **Dependencies**: Graph showing story order
3. **Parallel Opportunities**: Count of [P] tasks per phase
4. **All Phases**: Setup → Foundational → User Stories → Polish
5. **Verification Checklist**: How to mark each task complete

**Save**: `specs/$FEATURE/tasks.md`

### Step 6.2: Report Completion

**Output**:
```
✓ Task breakdown created: specs/<number>-<name>/tasks.md

Task Summary:
- Total tasks: 45
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 3 tasks
- Phase 3 (US P1): 10 tasks (2 tests, 5 impl, 3 verify)
- Phase 4 (US P2): 12 tasks (3 tests, 6 impl, 3 verify)
- Phase 5 (US P3): 8 tasks (2 tests, 4 impl, 2 verify)
- Phase 6 (Polish): 8 tasks

Parallel Opportunities:
- Setup: 3 of 4 tasks can run in parallel
- User Story P1: 2 test tasks can run in parallel
- User Story P2: 3 test tasks can run in parallel

Acceptance Criteria Coverage:
- Total ACs: 8
- Tests mapped: 8 (100% coverage)
- Each AC has ≥1 test task

Story Independence:
- ✓ Each story has independent test criteria
- ✓ Stories can be implemented in priority order (P1 → P2 → P3)
- ✓ Each story is demonstrable standalone

Constitutional Compliance:
- ✓ Article III: Tests before implementation (TDD)
- ✓ Article VII: Tasks organized by user story (not layer)
- ✓ Article VIII: Parallel tasks marked [P]

**Automatic Quality Gate**:
Running /audit command now for validation...

[Audit results will appear here]

If audit passes: Next Step: Run /implement plan.md
If audit fails: Fix CRITICAL issues first, then re-run /tasks
```

### Step 6.3: Update Master Todo with User Story Subtasks

Per @.claude/shared-imports/master-todo-utils.md, add subtasks to `todos/master-todo.md`:

```markdown
## Phase N: <Feature Name>
**Status**: ❌ TODO
**Spec**: `specs/$FEATURE/spec.md`
**Plan**: `specs/$FEATURE/plan.md`
**Tasks**: `specs/$FEATURE/tasks.md`

### User Stories (linked to tasks.md)
- [ ] US-1: <Story name> (P1) → `specs/$FEATURE/tasks.md#us-1`
- [ ] US-2: <Story name> (P2) → `specs/$FEATURE/tasks.md#us-2`
- [ ] US-3: <Story name> (P3) → `specs/$FEATURE/tasks.md#us-3`
```

---

## Anti-Patterns & Best Practices

**See:** @.claude/skills/generate-tasks/references/anti-patterns.md

**Critical Anti-Patterns to Avoid**:
- ❌ Layer-based organization ("All models", "All services")
- ❌ Tasks without [US#] story labels
- ❌ Skipping test tasks (Article III violation)
- ❌ Mixing multiple stories in one phase
- ❌ Creating <2 tests per story
- ❌ Forgetting [P] parallelization markers

**Best Practices**:
- ✓ Organize by user story (one phase per story)
- ✓ Label all tasks with [US#]
- ✓ Tests before implementation (TDD)
- ✓ Independent test criteria per story
- ✓ Mark parallel tasks with [P]
- ✓ Verify 100% AC coverage

---

## Example Task Breakdown

**See:** @.claude/skills/generate-tasks/examples/task-examples.md

**Complete Example**: User Authentication feature with 2 user stories (Registration, Login)

**Demonstrates**:
- Setup → Foundational → User Story Phases → Polish structure
- Test-first approach (Article III)
- Story-centric organization (Article VII)
- [P] parallelization markers (Article VIII)
- Independent test criteria per story
- 100% AC coverage with test task mapping

---

## Prerequisites

Before using this skill:
- ✅ spec.md exists (Article IV: specification-first)
- ✅ plan.md exists (Article IV: plan before tasks)
- ✅ PreToolUse hook validates both files exist (automatic enforcement)
- ✅ User stories with priorities defined in spec.md
- ✅ Acceptance criteria defined in plan.md (≥2 per story)
- ⚠️ Optional: data-model.md exists (for entity-based tasks)
- ⚠️ Optional: contracts/ exist (for API task breakdown)

## Dependencies

**Depends On**:
- **specify-feature skill** - Provides spec.md with user stories
- **create-implementation-plan skill** - MUST run before this skill (Article IV)
- **clarify-specification skill** - Should have resolved ambiguities before planning

**Integrates With**:
- **implement-and-verify skill** - Uses tasks.md output as implementation roadmap
- **/audit command** - Automatically invoked after task generation
- **/implement command** - Requires tasks.md to exist before execution

**Tool Dependencies**:
- Read tool (to load spec.md, plan.md, supporting docs)
- Write tool (to create tasks.md)

## Next Steps

After task generation completes, **automatic workflow progression**:

**Automatic Chain** (no manual intervention):
```
generate-tasks (creates tasks.md)
    ↓ (auto-invokes /audit)
/audit (validates cross-artifact consistency)
    ↓ (if PASS)
Ready for /implement
```

**User Action Required**:
- **If audit PASS**: Run `/implement plan.md` to begin implementation
- **If audit FAIL**: Fix CRITICAL issues in spec.md, plan.md, or tasks.md, then re-run generate-tasks

**Outputs Created**:
- `specs/$FEATURE/tasks.md` - User-story-organized task breakdown
- `YYYYMMDD-HHMM-audit-$FEATURE.md` - Quality gate validation report (automatic)

**Commands**:
- **/implement plan.md** - Begin implementation (after audit passes)
- **/audit $FEATURE** - Re-run audit if changes made to artifacts
- **/verify plan.md --story P1** - Verify individual story completion (during implementation)

## Agent Integration

This skill operates within the planner agent's workflow but does not directly invoke other agents.

### Relationship to Implementation Planner

**Context**: This skill is typically invoked BY the `create-implementation-plan` skill as part of automatic workflow progression.

**Execution**:
- Usually runs in main conversation context (not isolated agent)
- Can run within implementation-planner agent if plan creation and task generation combined
- Inherits context from previous workflow steps (spec.md, plan.md)

### Audit Agent (Indirect)

**When**: Automatically after tasks.md is created

**Agent**: None directly - `/audit` command may use specialized validation logic

**Delegation Method**: This skill automatically invokes `/audit` command via SlashCommand tool

```
generate-tasks skill (creates tasks.md)
    ↓ invokes
/audit command (SlashCommand tool)
    ↓ expands to
Validation workflow (constitution checks, consistency analysis)
    ↓ produces
audit report (PASS/FAIL with findings)
```

### Implementation Executor (Next Stage)

**When**: After audit passes, user runs `/implement`

**Agent**: executor-implement-verify

**Handover**: This skill prepares tasks.md which the executor agent consumes

**What Executor Receives** (from tasks.md):
- User stories organized by priority (P1, P2, P3...)
- Tasks per story with acceptance criteria
- Dependencies and blocking relationships
- Test strategy and verification approach

### Task Tool Usage

This skill does NOT directly use the Task tool. It:
1. Runs in main context or within planner agent
2. Invokes `/audit` via SlashCommand tool (automatic)
3. Prepares output for executor agent (consumed later)

**Design Rationale**:
- Task generation is deterministic (doesn't need agent isolation)
- Constitutional checks integrated into generation process
- Workflow orchestration via slash commands (cleaner than nested Task calls)

## Failure Modes

### Common Failures & Solutions

**1. plan.md does not exist (Article IV violation)**
- **Symptom**: PreToolUse hook blocks with "Cannot create tasks without implementation plan"
- **Solution**: Run create-implementation-plan skill or /plan command first
- **Prevention**: Follow SDD workflow order: /feature → /plan → /tasks → /implement

**2. User stories missing priorities (P1, P2, P3)**
- **Symptom**: Cannot organize tasks by story priority
- **Solution**: Update spec.md to add priority labels to all user stories
- **Guidance**: P1 = must-have MVP, P2 = important enhancements, P3 = nice-to-have

**3. Acceptance criteria insufficient (< 2 per story)**
- **Symptom**: Article III violation detected during task generation
- **Solution**: Update plan.md to add ≥2 acceptance criteria per user story
- **Requirement**: Each AC must be testable and independently verifiable

**4. Task organization by layer instead of story**
- **Symptom**: Article VII violation - tasks grouped by "All Models", "All Services", etc.
- **Solution**: Reorganize tasks by user story: Phase per story, tasks for that story only
- **Prevention**: Review @constitution.md Article VII before generating tasks

**5. Tests missing or after implementation tasks**
- **Symptom**: Article III violation - no test tasks OR test tasks after implementation
- **Solution**: Add test tasks for each AC, place BEFORE implementation tasks
- **Pattern**: Tests → Implementation → Verification (always this order)

**6. Parallel markers missing or incorrect**
- **Symptom**: Article VIII violation - no [P] markers OR [P] on dependent tasks
- **Solution**: Add [P] only to tasks with different files and no dependencies
- **Check**: Can T008 and T009 run simultaneously? Different files + no dependencies = [P]

**7. Story independence not verified**
- **Symptom**: User stories depend on each other, cannot be demoed standalone
- **Solution**: Add "Independent Test" criteria to each story phase
- **Requirement**: Each story must work without other stories implemented

**8. Audit invocation skipped**
- **Symptom**: tasks.md created but audit not run automatically
- **Solution**: Skill should invoke /audit command automatically (not ask user to run it)
- **Enforcement**: Article V (Template-Driven Quality) requires automatic quality gates

**9. Task IDs not sequential or story labels missing**
- **Symptom**: Tasks numbered T001, T010, T100 (gaps) OR no [US#] labels
- **Solution**: Use sequential T001, T002, T003... and add [US#] to all story-specific tasks
- **Example**: T008 [P] [US1] Write test for AC-P1-001

**10. Missing verification tasks per story**
- **Symptom**: No tasks to verify story completion, unclear when story is done
- **Solution**: Add verification phase to each story with tasks to run tests and validate
- **Pattern**: "Run all US# tests (must pass 100%)", "Test story independently"

## Related Skills & Commands

**Direct Integration**:
- **specify-feature skill** - Provides spec.md with user stories (required predecessor)
- **create-implementation-plan skill** - Provides plan.md with ACs and tech details (required predecessor)
- **implement-and-verify skill** - Uses tasks.md to execute implementation
- **/tasks command** - User-facing command that invokes this skill
- **/audit command** - Automatically invoked after this skill completes
- **/implement command** - Requires tasks.md to exist before running

**Workflow Context**:
- Position: **Phase 3** of SDD workflow (after planning, before implementation)
- Triggers: Automatically invoked by create-implementation-plan skill via SlashCommand tool
- Output: tasks.md with user-story-organized task breakdown

**Quality Gates**:
- **Automatic Audit**: /audit runs immediately after task generation
- **Article III Enforcement**: ≥2 ACs per story, tests before implementation
- **Article VII Enforcement**: Tasks organized by story (not layer)
- **Article VIII Enforcement**: [P] markers for parallelizable tasks

---

## Success Metrics

**Task Organization Quality:**
- 100% user-story-centric (Article VII compliance)
- 100% AC coverage (every AC has ≥1 test task)
- ≥2 ACs per user story (Article III requirement)
- All tasks labeled with [US#] for traceability

**Progressive Delivery:**
- Each story has independent test criteria
- Stories can be demoed without dependencies
- Clear priority order (P1 → P2 → P3)
- MVP (P1) implementable first

**Efficiency:**
- Parallel opportunities identified ([P] markers)
- Dependencies documented clearly
- Sequential tasks ordered correctly
- Audit passes on first generation

---

## Version

**Version:** 1.2.0
**Last Updated:** 2025-01-19
**Owner:** Claude Code Intelligence Toolkit

**Change Log**:
- v1.2.0 (2025-01-19): Added explicit SDD workflow context with 8-phase chain (Phase 6)
- v1.1.0 (2025-10-23): Refactored to progressive disclosure pattern (<500 lines)
- v1.0.0 (2025-10-22): Initial version with automatic audit enforcement
