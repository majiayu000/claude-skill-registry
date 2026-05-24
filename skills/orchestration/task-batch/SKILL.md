---
# VERSION: 2.88.0
name: task-batch
description: "Autonomous batch task execution with PRD parsing, task decomposition, and continuous execution until all tasks complete. Uses /orchestrator internally. Stops only for major failures (no internet, token limit, system crash). Use when: (1) processing task lists autonomously, (2) PRD-driven development, (3) batch feature implementation. Triggers: /task-batch, 'batch tasks', 'process PRD', 'run task queue'."
argument-hint: "<task-file.prq|prd-file.md|inline-tasks>"
user-invocable: true
context: fork
agent: orchestrator
allowed-tools:
  - Task
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - TeamCreate
  - TeamDelete
  - SendMessage
  - Read
  - Edit
  - Write
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__plugin_claude-mem_*
---

# /task-batch - Autonomous Batch Task Execution (v2.88)

**Continuous autonomous execution** of task lists with PRD parsing, automatic task decomposition, and completion validation. Runs until ALL tasks reach VERIFIED_DONE or major failure occurs.

Based on research from:
- [Sugar](https://github.com/roboticforce/sugar) - 24/7 autonomous layer for AI coding agents
- [Daedalus/Talos](https://github.com/internet-development/daedalus) - Task queue daemon with dependency resolution
- [Continuous Autonomous Task Loop Pattern](https://agentic-patterns.com/patterns/continuous-autonomous-task-loop-pattern/)
- [claude-queue](https://github.com/vasiliyk/claude-queue) - Priority-based task queuing

## Quick Start

```bash
# From PRD file
/task-batch docs/prd/feature-x.prq.md

# From task list file
/task-batch tasks/sprint-backlog.md

# Inline tasks (semicolon-separated)
/task-batch "Add authentication; Implement user profile; Add password reset"

# With priority ordering
/task-batch tasks/features.md --priority

# With specific teammates
/task-batch tasks/backend.md --teammates coder,reviewer,tester
```

## Core Design Principles

### 1. Continuous Autonomous Execution
- **NO user interaction** until all tasks complete (except critical failures)
- **Fresh context per task** - each task starts with clean context to avoid contamination
- **Auto-commit** after each VERIFIED_DONE task
- **Intelligent rate limit handling** - exponential backoff with configurable delays

### 2. Stop Conditions

| Condition | Action |
|-----------|--------|
| All tasks VERIFIED_DONE | **STOP** - Output summary, delete team |
| No internet connectivity | **STOP** - Report error, save state |
| Token limit reached | **STOP** - Save progress, report position |
| System crash/error | **STOP** - Emergency save, report diagnostics |
| Max iterations reached | **FAIL** - **CRITICAL ERROR**: This indicates infinite loop, report all incomplete tasks |
| **Tasks remaining at exit** | **FAIL** - **CRITICAL ERROR**: NEVER exit with pending tasks unless critical failure |
| **Normal user questions** | **CONTINUE** - Queue for end-of-batch response |

### ⚠️ CRITICAL RULE: NO PARTIAL SUCCESS

**The skill MUST NEVER report success with incomplete tasks.**

```
❌ WRONG: "Completed 10 of 17 tasks" → Summary → Exit 0
✅ RIGHT: "Completed 10 of 17 tasks" → Continue execution until ALL 17 done
✅ RIGHT: "Cannot continue due to [critical failure]" → Report error → Exit 1
```

If execution cannot continue (blocked dependencies, critical failure), the skill MUST:
1. Report explicit FAILURE status
2. List all incomplete tasks with reasons
3. Exit with non-zero code
4. Save state for manual recovery

### 3. Task Execution Model (MULTIPLE TASKS)

**CRITICAL: This skill handles MULTIPLE tasks, not just one task.**

```
+------------------------------------------------------------------+
|                    TASK-BATCH EXECUTION MODEL                     |
|                   (MULTIPLE TASKS - DEFAULT MODE)                 |
+------------------------------------------------------------------+
|                                                                   |
|   +----------+    +-------------+    +----------------+           |
|   |  PARSE   |--->| PRIORITIZE  |--->| DECOMPOSE      |           |
|   |  Input   |    | (optional)  |    | Complex Tasks  |           |
|   +----------+    +-------------+    +-------+--------+           |
|                                              |                    |
|   +------------------------------------------v---------------+   |
|   |              TASK QUEUE (N TASKS)                          |   |
|   |                                                            |   |
|   |   [Task1]    [Task2]    [Task3]    [Task4]    [TaskN]     |   |
|   |   Criteria  Criteria  Criteria  Criteria  Criteria       |   |
|   |   ✅ ✓✓✓    ✅ ✓✓✓    ⏳ ...     ⏳ ...     ⏳ ...        |   |
|   +---------------------------+-------------------------------+   |
|                               |                                   |
|   +---------------------------v-------------------------------+   |
|   |            EXECUTION LOOP (FOR EACH TASK)                  |   |
|   |                                                            |   |
|   |   FOR EACH task IN task_queue:                            |   |
|   |     +--------+   +------------+   +---------------+        |   |
|   |     | VALIDATE|-->| ORCHESTRATE|-->|CHECK CRITERIA|        |   |
|   |     | Criteria|   | (10-step)  |   | (ALL must ✓) |        |   |
|   |     +--------+   +------------+   +-------+-------+        |   |
|   |                                                  |         |   |
|   |                                    ALL MET? <--YES--NO-->  |   |
|   |                                        |        RETRY      |   |
|   |                                        v                   |   |
|   |                               +---------------+            |   |
|   |                               | VERIFIED_DONE |            |   |
|   |                               |  + NEXT TASK  |            |   |
|   |                               +---------------+            |   |
|   +------------------------------------------------------------+   |
+------------------------------------------------------------------+   |
|   |                                       YES<--+-->NO         |   |
|   |                                        |      |            |   |
|   |                         +--------------+      |            |   |
|   |                         v                     v            |   |
|   |                  +-----------+        +------------+       |   |
|   |                  | AUTO-COMMIT|        | RETRY      |       |   |
|   |                  | + NEXT    |        | (max 3)    |       |   |
|   |                  +-----------+        +------------+       |   |
|   |                                                            |   |
|   +------------------------------------------------------------+   |
|                                                                   |
+------------------------------------------------------------------+
```

## Input Formats

### 1. PRD File Format (.prq.md or .md)

```markdown
# Feature: User Authentication

## Priority: HIGH

## Overview
Implement OAuth2 authentication with Google provider.

## Tasks
- [ ] P1: Create OAuth2 service module
- [ ] P1: Add Google OAuth provider configuration
- [ ] P2: Implement login callback handler
- [ ] P2: Add session management
- [ ] P3: Create authentication middleware
- [ ] P3: Write unit tests

## Dependencies
- P2 tasks depend on P1 tasks completion

## Acceptance Criteria
- Users can login with Google
- Sessions persist for 7 days
- All tests pass
```

### 2. Task List Format

```markdown
# Sprint Backlog - Week 12

## Backend Tasks
1. [P1] Implement rate limiting with Redis
2. [P1] Add input validation to all endpoints
3. [P2] Create API documentation with OpenAPI
4. [P2] Add request logging middleware

## Frontend Tasks
5. [P1] Fix login form validation
6. [P2] Add loading states to buttons
7. [P3] Implement dark mode toggle
```

### 3. Inline Tasks

```bash
/task-batch "Add user schema; Create CRUD endpoints; Add validation"
```

### 4. JSON Task File

```json
{
  "batch_name": "auth-feature",
  "tasks": [
    {
      "id": "auth-001",
      "description": "Create OAuth2 service",
      "priority": 1,
      "dependencies": [],
      "acceptance_criteria": ["Module exists", "Exports configured client"]
    },
    {
      "id": "auth-002",
      "description": "Add Google provider",
      "priority": 1,
      "dependencies": ["auth-001"],
      "acceptance_criteria": ["Google OAuth configured", "Test passes"]
    }
  ],
  "config": {
    "max_retries": 3,
    "auto_commit": true,
    "stop_on_failure": false
  }
}
```

## Execution Workflow

### Phase 1: PARSE

Parse input into structured task list:

```yaml
# Parse logic
Input Type Detection:
  - .prq.md or .md ending → PRD Parser
  - .json ending → JSON Parser
  - tasks/ directory → Multi-file Parser
  - Inline text → Inline Parser

Task Extraction:
  - Extract task descriptions
  - Parse priority markers (P1/P2/P3 or HIGH/MEDIUM/LOW)
  - Identify dependencies
  - Extract acceptance criteria
```

### Phase 2: PRIORITIZE (Optional)

When `--priority` flag is set:

```yaml
Priority Rules:
  1. Explicit priority markers (P1 > P2 > P3)
  2. Dependency order (dependencies first)
  3. File order (as listed in input)
  4. Estimated effort (smaller tasks first when same priority)
```

### Phase 3: DECOMPOSE

For tasks with complexity > 6:

```yaml
Decomposition Rules:
  - Split into subtasks if:
    - Task has multiple deliverables
    - Task spans multiple files
    - Task requires different expertise
  - Create subtask dependencies
  - Preserve original acceptance criteria
```

### Phase 4: EXECUTE (Main Loop)

```bash
# Pseudocode for execution loop
task_queue = parse_and_prioritize(input)
completed_tasks = []
failed_tasks = []
iteration = 0
max_iterations = len(task_queue) * 5  # Safety limit

while task_queue and iteration < max_iterations:
    # Rate limit check
    if rate_limit_detected():
        sleep(exponential_backoff())
        continue

    # Select next task (respecting dependencies)
    task = select_next_task(task_queue, completed_tasks)

    if task is None:
        # All remaining tasks blocked - THIS IS A FAILURE
        blocked_tasks = identify_blocked_reasons(task_queue, completed_tasks)
        report_failure("BLOCKED", blocked_tasks)
        exit 1  # FAILURE - cannot continue

    # Fresh context per task (via new subagent)
    result = execute_with_orchestrator(task)

    if result == VERIFIED_DONE:
        completed_tasks.append(task)
        task_queue.remove(task)
        auto_commit(task)

        # Update dependent tasks
        update_dependencies(task_queue, task)
    else:
        if task.retry_count < MAX_RETRIES:
            task.retry_count += 1
            # Re-queue with feedback
            task.feedback = result.errors
        else:
            failed_tasks.append(task)
            # DO NOT break - continue with remaining tasks
            # Unless stop_on_failure is explicitly set
            if config.stop_on_failure:
                break

    iteration++

# ══════════════════════════════════════════════════════════════════
# CRITICAL: FINAL VALIDATION - NO PARTIAL SUCCESS ALLOWED
# ══════════════════════════════════════════════════════════════════
if len(task_queue) > 0:
    # THERE ARE STILL PENDING TASKS - THIS IS A FAILURE
    print("❌ BATCH FAILED: Incomplete tasks remain")
    print(f"   Completed: {len(completed_tasks)}")
    print(f"   Pending:   {len(task_queue)}")
    print(f"   Failed:    {len(failed_tasks)}")
    for task in task_queue:
        print(f"   - {task.id}: {task.description}")
    exit 1  # EXPLICIT FAILURE

if len(failed_tasks) > 0:
    # SOME TASKS FAILED AFTER MAX RETRIES
    print("❌ BATCH FAILED: Tasks exceeded max retries")
    for task in failed_tasks:
        print(f"   - {task.id}: {task.description}")
        print(f"     Error: {task.last_error}")
    exit 1  # EXPLICIT FAILURE

# ALL TASKS COMPLETED SUCCESSFULLY
output_summary(completed_tasks, [])
exit 0  # SUCCESS
```

### Phase 5: REPORT

```yaml
Summary Output:
  - Total tasks: N
  - Completed: M
  - Failed: X
  - Skipped: Y (blocked by failures)

  - For each task:
    - Status: VERIFIED_DONE | FAILED | SKIPPED
    - Duration: XX minutes
    - Files modified: [list]
    - Commits: [sha1, sha2, ...]

  - For failed tasks:
    - Error details
    - Retry attempts
    - Suggested fixes
```

## Team Coordination (Agent Teams)

### Team Creation

```yaml
# Automatic on skill invocation
TeamCreate:
  team_name: "task-batch-{timestamp}"
  description: "Batch execution: {batch_name}"
  agent_type: "orchestrator"
```

### Task Distribution

```yaml
# Create tasks in shared list
TaskCreate:
  subject: "{task_description}"
  description: "{full_task_details}"
  activeForm: "Executing: {task_description}"
  metadata:
    priority: "{priority}"
    dependencies: ["{dep_task_ids}"]
    acceptance_criteria: ["{criteria}"]

# Assign to appropriate teammate
TaskUpdate:
  taskId: "{id}"
  owner: "ralph-coder"  # or ralph-reviewer, ralph-tester
```

### Teammate Spawning

```yaml
# Spawn teammates based on task type
Task:
  subagent_type: "ralph-coder"
  team_name: "task-batch-{timestamp}"
  name: "batch-coder"
  prompt: |
    Execute task: {task_description}

    Acceptance Criteria:
    {acceptance_criteria}

    Context: Fresh execution, no prior context.

    Execute until VERIFIED_DONE or max retries reached.
```

### Hook Integration

| Hook | Purpose | Exit 2 Behavior |
|------|---------|-----------------|
| `teammate-idle-quality-gate.sh` | Quality check before idle | Keep working with feedback |
| `task-completed-quality-gate.sh` | Validate before completion | Prevent completion, retry |
| `ralph-subagent-start.sh` | Load Ralph context | - |
| `batch-progress-tracker.sh` | Track batch progress | Continue if tasks remain |

### Progress Tracking

```yaml
# Progress file: .ralph/batch/{batch_id}/progress.json
{
  "batch_id": "batch-20260215-123456",
  "started": "2026-02-15T12:00:00Z",
  "total_tasks": 10,
  "completed": 5,
  "failed": 1,
  "current_task": "auth-006",
  "estimated_completion": "2026-02-15T14:30:00Z"
}
```

## Error Handling

### Rate Limit Handling

```yaml
Rate Limit Detection:
  - API response: 429 Too Many Requests
  - Error message contains "rate limit"
  - Timeout exceeded

Recovery:
  - Initial backoff: 60 seconds
  - Max backoff: 300 seconds (5 minutes)
  - Backoff multiplier: 2x
  - Max retries: 5

  On max retries exceeded:
    - Save state
    - Report error
    - STOP batch execution
```

### Task Failure Handling

```yaml
Task Failure Options:
  stop_on_failure: false  # Continue with remaining tasks
  stop_on_failure: true   # Stop entire batch

Failure Recovery:
  1. Log error details
  2. Capture current state
  3. If retry_count < MAX_RETRIES:
     - Add feedback to task
     - Re-queue for retry
  4. Else:
     - Mark as FAILED
     - Skip dependent tasks
```

### Critical Failure Detection

```yaml
Critical Failures (STOP immediately):
  - No network connectivity (ping failed)
  - Token limit reached (>95% context used)
  - System crash (unhandled exception)
  - Authentication failure
  - Repository corruption

Non-Critical Failures (CONTINUE):
  - Single task failure (if stop_on_failure=false)
  - Test failure (triggers retry)
  - Lint errors (triggers retry)
  - Type errors (triggers retry)
```

## CLI Commands

```bash
# Basic batch execution
ralph batch tasks/features.md

# With priority ordering
ralph batch tasks/sprint.md --priority

# Stop on first failure
ralph batch tasks/critical.md --stop-on-failure

# Resume interrupted batch
ralph batch --resume batch-20260215-123456

# Check batch status
ralph batch --status batch-20260215-123456

# List running batches
ralph batch --list

# Cancel running batch
ralph batch --cancel batch-20260215-123456
```

## Configuration

### Default Configuration

```yaml
# ~/.ralph/config/batch.yaml
batch:
  max_iterations_multiplier: 5  # max_iter = task_count * multiplier
  max_retries_per_task: 3
  auto_commit: true
  stop_on_failure: false
  priority_enabled: false

rate_limits:
  initial_backoff_seconds: 60
  max_backoff_seconds: 300
  backoff_multiplier: 2
  max_retries: 5

teammates:
  default: [coder, reviewer]
  complex: [coder, reviewer, tester]
  critical: [coder, reviewer, tester, security]

hooks:
  progress_tracking: true
  quality_gates: true
```

### Per-Batch Override

```yaml
# In task file frontmatter
---
batch:
  max_retries: 5
  stop_on_failure: true
  teammates: [coder, tester]
---
```

## Completion Criteria

### VERIFIED_DONE (Per Task)

Each task requires ALL:
1. Implementation complete
2. CORRECTNESS passed (syntax, logic)
3. QUALITY passed (types, linting)
4. SECURITY passed (no vulnerabilities)
5. Acceptance criteria verified
6. Auto-commit successful

### BATCH_COMPLETE (Full Batch)

Requires ALL:
1. All tasks processed (VERIFIED_DONE or FAILED)
2. Summary report generated
3. Git history clean (commits for each task)
4. Team deleted
5. Progress file archived

## Anti-Patterns

- **NEVER** stop for non-critical user questions (queue them)
- **NEVER** use infinite loops (always set max_iterations)
- **NEVER** skip quality gates (defeats VERIFIED_DONE)
- **NEVER** share context between tasks (contamination risk)
- **NEVER** ignore rate limits (will cause failures)
- **NEVER** commit without VERIFIED_DONE (incomplete work)
- **⚠️ CRITICAL: NEVER report success with incomplete tasks**

### The "Partial Success" Anti-Pattern

```
❌ WRONG BEHAVIOR:
  Output: "Completed Tasks (10 of 17)"
  Output: "Remaining Tasks (7)"
  Action: Exit 0 (success)

✅ CORRECT BEHAVIOR:
  Option A: Continue execution until ALL 17 tasks complete
  Option B: If cannot continue:
    Output: "❌ BATCH FAILED: Cannot continue"
    Output: "Completed: 10, Pending: 7, Failed: 0"
    Output: "Reason: [blocked dependency | critical error | token limit]"
    Exit: 1 (failure)
```

If you find yourself about to output a summary with remaining tasks:
1. STOP - do not output success
2. Either continue execution OR report explicit failure
3. Partial completion = FAILURE, not success

## Comparison: /task-batch vs /orchestrator vs /loop

| Feature | /task-batch | /orchestrator | /loop |
|---------|-------------|---------------|-------|
| **Input** | Multiple tasks | Single task | Single task |
| **Execution** | Continuous until all done | Single workflow | Iterative refinement |
| **User Interaction** | Minimal (critical only) | Full clarification | Iteration prompts |
| **Stop Condition** | All complete OR critical failure | VERIFIED_DONE | VERIFIED_DONE or max iter |
| **Task Decomposition** | Automatic | Manual (in plan) | N/A |
| **PRD Support** | Native | Via clarify | N/A |
| **Priority Ordering** | Yes | No | No |
| **Best For** | Batch features, PRD execution | Complex single tasks | Quality refinement |

## Agent Teams Integration (v2.88)

**Optimal Scenario**: Integrated (Agent Teams + Custom Subagents)

### Why Scenario C for This Skill
- **Batch coordination** requires tracking multiple tasks across teammates
- **Quality gates** essential for VERIFIED_DONE on each task
- **Specialized agents** (ralph-coder, ralph-reviewer, ralph-tester) for different task types
- **Shared task list** enables dependency management and progress tracking
- **Continuous execution** benefits from team coordination without user intervention

### Configuration
1. **TeamCreate**: Create team "task-batch-{batch-id}" on invocation
2. **TaskCreate**: Create task for each item in batch
3. **Spawn**: Use ralph-coder for implementation, ralph-reviewer for validation
4. **Hooks**: TeammateIdle + TaskCompleted for quality validation
5. **Coordination**: Shared task list at ~/.claude/tasks/task-batch-{id}/

### VERIFIED_DONE Guarantee with Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `teammate-idle-quality-gate.sh` | TeammateIdle | Prevent idle if tasks remain |
| `task-completed-quality-gate.sh` | TaskCompleted | Validate task before marking complete |
| `ralph-subagent-stop.sh` | SubagentStop | Quality gate when teammate stops |
| `batch-progress-tracker.sh` | PostToolUse | Update batch progress file |

**Exit 2 Behavior**: Hooks return exit 2 to force continuation when:
- More tasks remain in queue
- Quality gates failed but retries available
- Dependency tasks not yet complete

## Related Skills

- `/orchestrator` - Base 10-step workflow (used internally)
- `/loop` - Iterative refinement pattern
- `/gates` - Quality validation gates
- `/clarify` - Requirement clarification (used for PRD parsing)
- `/retrospective` - Post-batch analysis


## Action Reporting (v2.93.0)

**Esta skill genera reportes automáticos completos** para trazabilidad:

### Reporte Automático

Cuando esta skill completa, se genera automáticamente:

1. **En la conversación de Claude**: Resultados visibles
2. **En el repositorio**: `docs/actions/task-batch/{timestamp}.md`
3. **Metadatos JSON**: `.claude/metadata/actions/task-batch/{timestamp}.json`

### Contenido del Reporte

Cada reporte incluye:
- ✅ **Summary**: Descripción de la tarea ejecutada
- ✅ **Execution Details**: Duración, iteraciones, archivos modificados
- ✅ **Results**: Errores encontrados, recomendaciones
- ✅ **Next Steps**: Próximas acciones sugeridas

### Ver Reportes Anteriores

```bash
# Listar todos los reportes de esta skill
ls -lt docs/actions/task-batch/

# Ver el reporte más reciente
cat $(ls -t docs/actions/task-batch/*.md | head -1)

# Buscar reportes fallidos
grep -l "Status: FAILED" docs/actions/task-batch/*.md
```

### Generación Manual (Opcional)

```bash
source .claude/lib/action-report-lib.sh
start_action_report "task-batch" "Task description"
# ... ejecución ...
complete_action_report "success" "Summary" "Recommendations"
```

### Referencias del Sistema

- [Action Reports System](docs/actions/README.md) - Documentación completa
- [action-report-lib.sh](.claude/lib/action-report-lib.sh) - Librería helper
- [action-report-generator.sh](.claude/lib/action-report-generator.sh) - Generador

- [Sugar - Autonomous AI Coding](https://github.com/roboticforce/sugar)
- [Daedalus/Talos - Task Queue Daemon](https://github.com/internet-development/daedalus)
- [Continuous Autonomous Task Loop Pattern](https://agentic-patterns.com/patterns/continuous-autonomous-task-loop-pattern/)
- [claude-queue - Priority Task Queuing](https://github.com/vasiliyk/claude-queue)
- [Awesome Agentic Patterns](https://github.com/nibzard/awesome-agentic-patterns)
- [Unified Architecture v2.88](docs/architecture/UNIFIED_ARCHITECTURE_v2.88.md)
- [Claude Code Agent Teams Documentation](https://code.claude.com/docs/en/agent-teams)
