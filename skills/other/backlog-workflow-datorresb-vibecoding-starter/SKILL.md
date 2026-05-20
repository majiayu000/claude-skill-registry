---
name: backlog-workflow
description: Project-agnostic workflow guidance for Backlog.md MCP task management. Covers search-first protocol, scope assessment, task creation standards, lifecycle management, and cross-session coordination.
---

# Backlog.md MCP Workflow Skill

## Core Principle: Track Commitments, Not Activity

**Backlog tracks what will be built.** Use it when work requires planning, decisions, or coordination across sessions. Skip it for trivial mechanical changes that can be completed immediately.

**Use Backlog when:**
- Work requires planning or architectural decisions
- Multiple deliverables need coordination
- Other sessions might duplicate effort
- Progress tracking benefits stakeholders
- Work spans multiple sessions

**Skip Backlog when:**
- Single trivial change (typo fix, simple config update)
- Immediate execution with no planning needed
- Work completes in < 5 minutes
- No coordination required

## Search-First Protocol (CRITICAL)

**ALWAYS search before creating tasks.** Duplicate tasks waste effort and create confusion.

**Three-step search:**

1. **Keyword search:**
   ```
   task_search(query="relevant keywords", limit=20)
   ```

2. **Status filter:**
   ```
   task_list(status="To Do", limit=50)
   task_list(status="In Progress", limit=50)
   ```

3. **Label filter (if applicable):**
   ```
   task_list(labels=["essay", "infrastructure"], limit=30)
   ```

**When you find similar work:**
- Same goal, different approach → Comment on existing task, don't create duplicate
- Related but distinct → Create new task with dependency on existing
- Truly unique → Create new task, reference related tasks in description

**No search results → Proceed with task creation**

## Scope Assessment: Single Task vs Epic

**Decision framework:**

| Indicator | Single Task | Epic + Subtasks |
|-----------|-------------|-----------------|
| Deliverables | One clear output | Multiple distinct outputs |
| Parallelization | No independent components | Components can run in parallel |
| Duration | < 4 hours total | > 4 hours or multi-session |
| Dependencies | Linear execution | Some subtasks have dependencies |
| Coordination | One person/session | Multiple sessions or models |

**Single Task Pattern:**
- Clear deliverable (e.g., "Fix typography bug in essay paragraphs")
- Straightforward execution
- Completed in one session

**Epic Pattern:**
- Multiple deliverables (e.g., "Essay 12: Complete 6-step workflow")
- Subtasks can run in parallel (e.g., multiple essays' research phase)
- Requires coordination across sessions or models

**When in doubt:** Start with single task. Split into epic if scope grows during planning.

## Task Creation Standards

**Title format:** `[Action] [Target] [Context if needed]`

Good: "Create essay-technical-depth Skill (Step 1.5)"
Bad: "Work on skills" (vague action and target)

**Description template:**

```markdown
## Goal
[What will be accomplished - one sentence]

## Context
[Why this matters - link to project goals]

## Deliverables
- [Specific output 1 with file path]
- [Specific output 2 with criteria]

## Approach
[High-level implementation strategy - optional but recommended]
```

**Acceptance criteria (measurable):**

Good:
- [ ] File `/path/to/output.md` exists with required sections
- [ ] All 5 quality standards verified against checklist
- [ ] Tests pass and changes committed with task ID reference

Bad:
- [ ] Code works (not measurable)
- [ ] Quality is good (subjective)

**Dependencies:**
- List task IDs that must complete before this task starts
- Use Backlog task IDs (e.g., `task-35.1`, `task-37.2`)
- Document WHY dependency exists (helps future sessions understand blocking)

**Assignee (model assignment):**
- `Haiku` - Simple search/compile work (with Skills for quality)
- `Sonnet` - Structure/analysis requiring synthesis
- `Opus` - Complex reasoning, scholarly depth, maximum insight
- Assignee = recommendation, not requirement (delegate to appropriate model)

## Task Lifecycle Management

**Status transitions:**

```
To Do → In Progress → Done
```

**Critical rules:**

1. **Mark In Progress BEFORE starting work**
   ```
   task_edit(id="task-X", status="In Progress")
   ```

2. **Only ONE task In Progress per session** (focus)

3. **Mark Done IMMEDIATELY after completing**
   ```
   task_edit(id="task-X", status="Done")
   ```

4. **Use task_complete for archival** (moves to completed folder)
   ```
   task_complete(id="task-X")
   ```

**Task notes for session handoff:**

```
task_edit(
  id="task-X",
  notesAppend=[
    "Commit abc123: Implemented feature X",
    "Blocked on task-Y completion for integration testing",
    "Next: Run full test suite after task-Y merges"
  ]
)
```

**Implementation plan documentation:**

```
task_edit(
  id="task-X",
  planSet="1. Research existing patterns\n2. Draft implementation\n3. Test with Essay 6\n4. Commit with task ID"
)
```

## Coordinating Across Sessions

**Mental model:** Other Claude sessions = team members working in parallel.

**Before starting work:**

1. **Check assignees:**
   ```
   task_view(id="task-X")
   ```
   - Already assigned to another model/session? Don't duplicate effort
   - Unassigned? Assign to yourself before starting

2. **Check status:**
   - `In Progress` by another session? Coordinate in task notes
   - `To Do` and no assignee? Safe to claim

3. **Check dependencies:**
   ```
   task_view(id="task-X")
   ```
   - Review `dependencies` field
   - Verify blocking tasks are Done before starting

**Communication via task notes:**

```
task_edit(
  id="task-X",
  notesAppend=[
    "[Session A] Started implementation, 60% complete",
    "[Session B] Waiting for Session A to finish before integration testing"
  ]
)
```

**Parallel work pattern:**

```
Epic: Essay 12 Complete
├── task-12.1 Research (Haiku) - No deps → START NOW
├── task-12.1.5 Technical Analysis (Sonnet) - Deps: 12.1 → WAIT
├── task-12.2 First Draft (Sonnet) - Deps: 12.1, 12.1.5 → WAIT
└── task-12.3 Critique (Opus) - Deps: 12.2 → WAIT
```

Multiple essays can do Step 1 (research) in parallel:
- Essay 12 research (task-12.1)
- Essay 3 research (task-3.1)
- Essay 5 research (task-5.1)

All three can run simultaneously (no dependencies between essays).

## Epic Structure Pattern

**Template:**

```
Epic (Parent): [High-level goal]
├── Subtask 1: [Component A] (Dependencies: none)
├── Subtask 2: [Component B] (Dependencies: none)
├── Subtask 3: [Integration] (Dependencies: 1, 2)
└── Subtask 4: [Verification] (Dependencies: 3)
```

**Real example:**

```
Epic: Essay 12 - AI-Native Development (6-step workflow)
├── task-12.1: Research Compilation (Step 1) - Deps: none
├── task-12.1.5: Technical Deep-Dive (Step 1.5) - Deps: task-12.1
├── task-12.2: First Draft (Step 2) - Deps: task-12.1, task-12.1.5
├── task-12.3: Critique (Step 3) - Deps: task-12.2
├── task-12.4: Final Draft (Step 4) - Deps: task-12.3
└── task-12.5: Publication-Ready (Step 5) - Deps: task-12.4
```

**Parallelization opportunities:**

Across epics (different essays):
- All essay research tasks (Step 1) can run in parallel
- All technical analysis tasks (Step 1.5) can run in parallel after research completes
- All first drafts (Step 2) can run in parallel after prerequisites complete

Within epic:
- If subtasks have no dependencies, launch multiple subagents simultaneously
- Example: UI component + API endpoint can be built in parallel

**Creating epic structure in Backlog:**

1. **Create parent epic:**
   ```
   task_create(
     title="Essay 12: AI-Native Development (Complete 6-step workflow)",
     description="...",
     labels=["essay", "epic"],
     priority="high"
   )
   ```

2. **Create subtasks with parentTaskId:**
   ```
   task_create(
     title="Essay 12.1: Research Compilation (Step 1)",
     parentTaskId="task-12",
     dependencies=[],
     assignee=["Haiku"]
   )

   task_create(
     title="Essay 12.1.5: Technical Deep-Dive (Step 1.5)",
     parentTaskId="task-12",
     dependencies=["task-12.1"],
     assignee=["Sonnet"]
   )
   ```

## Quality Checklist Before Marking Done

**Before `task_edit(status="Done")`:**

- [ ] All deliverables specified in task description created
- [ ] All acceptance criteria met (measurable verification)
- [ ] Changes committed to git with task ID reference (e.g., `[task-12.1] Essay 12 Research`)
- [ ] Task notes updated with commit hash and completion summary
- [ ] Dependencies verified (this task no longer blocks other tasks)
- [ ] Output reviewed against quality standards (if applicable)

**Git commit pattern:**

```bash
git commit -m "[task-12.1] Essay 12 Research Compilation

Compiled comprehensive research with RAND, MIT, BCG sources. Full citations verified against essay-research-compilation Skill standards."
```

**Task completion note:**

```
task_edit(
  id="task-12.1",
  status="Done",
  notesAppend=["Commit abc123: Research compilation complete with 100% citation coverage. Ready for Step 1.5."]
)
```

## Common Patterns

**Pattern 1: Sequential workflow (one essay)**

```
Step 1 (Research) → Step 1.5 (Technical) → Step 2 (Draft) → Step 3 (Critique) → Step 4 (Final) → Step 5 (Publish)
```

Each step depends on previous step completing. No parallelization within single essay.

**Pattern 2: Parallel workflows (multiple essays)**

```
Essay A Step 1 ┐
Essay B Step 1 ├─ All run in parallel
Essay C Step 1 ┘

After all complete:

Essay A Step 1.5 ┐
Essay B Step 1.5 ├─ All run in parallel
Essay C Step 1.5 ┘
```

Maximize throughput by running same step across multiple essays simultaneously.

**Pattern 3: Mixed parallel/sequential**

```
Epic: Infrastructure Upgrade
├── Database migration (Subtask 1) - Independent
├── API refactor (Subtask 2) - Independent
├── Integration tests (Subtask 3) - Depends on 1 AND 2
└── Deployment (Subtask 4) - Depends on 3
```

Subtasks 1 and 2 run in parallel. Subtask 3 waits for both. Subtask 4 waits for 3.

**Pattern 4: ML Project (4-session workflow)**

```
Epic: [Project Name] - ML Pipeline
├── Session 1: ETL (Data loading, validation, split) - Gate G1
├── Session 2: EDA (Profiling, baseline, features) - Gate G2, Deps: Session 1
├── Session 3: MODELING (Ideation, training, champion) - Gates G3/G4, Deps: Session 2
└── Session 4: DELIVERY (Test eval, SHAP, reports) - Gate G5, Deps: Session 3
```

**ML project task structure:**

```
task_create(
  title="[Project Name] - ML Pipeline",
  description="4-session ML workflow: [problem statement]

  ## Goal
  [Business objective and success criteria]

  ## Data
  [Data sources, target column, problem type]

  ## Sessions
  - Session 1 (ETL): Load, validate, split data
  - Session 2 (EDA): Profile data, establish baseline
  - Session 3 (MODELING): Feature engineering, train models
  - Session 4 (DELIVERY): Test evaluation, reports
  ",
  labels=["ml-project", "4-session"],
  priority="high",
  acceptanceCriteria=[
    "Session 1 (ETL): G1 passed - Data loaded and split",
    "Session 2 (EDA): G2 passed - Baseline established",
    "Session 3 (MODELING): G3/G4 passed - Champion model beats baseline",
    "Session 4 (DELIVERY): G5 passed - Test evaluation complete"
  ]
)
```

**Session execution pattern:**

Each session follows this protocol:

1. **Start session (fresh chat):**
   ```
   task_search(query="[project-name]")
   task_edit(
     id="task-X",
     status="In Progress",
     labels=["ml-project", "session-N-<phase>"],
     notesAppend=["Starting Session N (<PHASE>) - <timestamp>"]
   )
   ```

2. **Execute session work:** Follow session-specific skill guidance

3. **End session (commit + update):**
   ```
   git commit -m "[task-X] [PHASE] Description

   - Key deliverables
   - Gate status: PASSED"

   task_edit(
     id="task-X",
     notesAppend=[
       "Session N (<PHASE>) completed - commit: <hash>",
       "Gate G<N>: PASSED",
       "Key metrics: <metric>: <value>",
       "Next: Session <N+1> in fresh chat"
     ],
     acceptanceCriteriaCheck=[<N>]
   )
   ```

**Knowledge transfer between sessions:**

- **Session 1 → 2:** `01_etl_summary.md`, `project_context.json`
- **Session 2 → 3:** `02_eda_summary.md`, `eda_handoff.json` (critical metrics)
- **Session 3 → 4:** `03_modeling_summary.md`, `modeling_handoff.json` (champion model)

Task notes supplement handoff files with session-specific context (blockers, decisions, learnings).

## Troubleshooting

**Problem: Can't find existing task**

Solution: Expand search (remove filters, try synonyms, check archived tasks)

**Problem: Task blocked by dependency**

Solution: Check dependency status with `task_view(id="blocking-task-id")`. If blocking task stalled, communicate in notes or escalate.

**Problem: Multiple sessions working on same task**

Solution: First session to mark "In Progress" owns the task. Other sessions should coordinate via task notes or find different work.

**Problem: Epic too large to track**

Solution: Break into smaller epics or use milestones for grouping. Each epic should represent ~1-2 weeks of work maximum.

**Problem: Task scope grew during execution**

Solution:
1. Complete original task scope
2. Mark original task Done
3. Create new task for expanded scope with dependency on completed task

## MCP Tool Reference

**Search:**
- `task_search(query="keywords", limit=20)` - Fuzzy search title/description
- `task_list(status="To Do", limit=50)` - Filter by status
- `task_list(labels=["essay"], limit=30)` - Filter by label

**CRUD:**
- `task_create(title, description, acceptanceCriteria, dependencies, assignee, priority, labels)`
- `task_view(id="task-X")` - View full task details
- `task_edit(id, status, notesAppend, planSet, ...)` - Update task
- `task_complete(id="task-X")` - Archive to completed folder

**Workflow:**
- `task_edit(id, status="In Progress")` - Claim task
- `task_edit(id, status="Done")` - Mark complete
- `task_edit(id, notesAppend=["Session update"])` - Communicate progress
- `task_edit(id, planSet="1. Step\n2. Step")` - Document approach

**Dependencies:**
- Set during creation: `dependencies=["task-X", "task-Y"]`
- Update later: `task_edit(id, dependencies=["task-X", "task-Y"])`
- Check blocking: `task_view(id)` and inspect dependencies field
