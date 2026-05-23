---
name: phase-7-finalize
description: Complete plan execution with git workflow and PR management
user-invocable: false
allowed-tools: Read, Bash, Glob, Skill, Task
---

# Phase Finalize Skill

**Role**: Finalize phase skill. Handles shipping workflow (commit, push, PR) and plan completion. Verification has already completed in phase-6-verify.

**Key Pattern**: Shipping-focused execution. No verification steps—all quality checks run in phase-6-verify before reaching this phase.

## When to Activate This Skill

Activate when:
- Verify phase has completed (all quality checks passed)
- Ready to commit and potentially create PR
- Plan is in `7-finalize` phase

---

## Phase Position in 7-Phase Model

```
1-init → 2-refine → 3-outline → 4-plan → 5-execute → 6-verify → 7-finalize
                                              ↑                       │
                                              └───────────────────────┘
                                              (loop on PR issues)
```

**Iteration limit**: 3 cycles max for PR issue resolution.

---

## Configuration Source

Finalize configuration comes from marshal.json phase sections:

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  plan phase-7-finalize get --trace-plan-id {plan_id}
```

Cross-phase settings (also from marshal.json):
```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  plan phase-5-execute get --trace-plan-id {plan_id}
```

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  plan phase-1-init get --trace-plan-id {plan_id}
```

**Config Fields Used**:

| Source | Field | Description |
|--------|-------|-------------|
| phase-7-finalize | `1_commit_push` | Whether to commit and push |
| phase-7-finalize | `2_create_pr` | Whether to create a pull request |
| phase-7-finalize | `3_automated_review` | Whether to run CI review |
| phase-7-finalize | `4_sonar_roundtrip` | Whether to run Sonar analysis |
| phase-7-finalize | `5_knowledge_capture` | Whether to capture learnings |
| phase-7-finalize | `6_lessons_capture` | Whether to record lessons |
| phase-7-finalize | `max_iterations` | Maximum finalize-verify loops |
| phase-5-execute | `commit_strategy` | per_deliverable/per_plan/none |
| phase-1-init | `branch_strategy` | feature/direct |

---

## Operation: finalize

**Input**: `plan_id`

### Step 0: Log Phase Start

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[STATUS] (pm-workflow:phase-7-finalize) Starting finalize phase"
```

### Step 1: Read Configuration

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  plan phase-7-finalize get --trace-plan-id {plan_id}
```

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  plan phase-5-execute get --trace-plan-id {plan_id}
```

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  plan phase-1-init get --trace-plan-id {plan_id}
```

Also read references context for branch and issue information:

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references get-context \
  --plan-id {plan_id}
```

Returns: `branch`, `base_branch`, `issue_url`, `build_system`, and file counts in a single call.

**After reading configuration**, log the finalize strategy decision:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-workflow:phase-7-finalize) Finalize strategy: commit={commit_strategy}, PR={create_pr}, branch={branch_strategy}"
```

### Step 2: Conditional Commit Workflow

**If `commit_strategy == none`**: Skip commit entirely.

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-workflow:phase-7-finalize) Commit skipped: commit_strategy=none"
```

Proceed directly to Step 3.

**If `commit_strategy == per_deliverable`**: Only commit if there are uncommitted changes remaining (some changes may already be committed per-deliverable during execute phase).

**If `commit_strategy == per_plan`**: Commit all changes as a single commit (current default behavior).

For `per_deliverable` and `per_plan`, load the git-workflow skill:

```
Skill: pm-workflow:workflow-integration-git
```

The git-workflow skill handles:
- Artifact detection and cleanup (*.class, *.temp files)
- Commit message generation following conventional commits
- Stage, commit, and push operations

**Parameters** (from config and request):
- `message`: Generated from request.md summary
- `push`: true (always push in finalize)
- `create-pr`: from `create_pr` config field

### Step 3: Create PR (if enabled)

If `create_pr == true`, the git-workflow skill creates the PR with:
- Title from request.md
- Body using `templates/pr-template.md`
- Issue link from references.toon (`Closes #{issue}` if present)

### Step 4: Automated Review (if PR created)

If PR was created:

```
Skill: pm-workflow:workflow-integration-ci
```

This monitors CI status and handles review comments.

**On findings** (CI failures, review comments):
1. Create fix tasks via manage-tasks
2. Loop back to phase-5-execute (iteration + 1)
3. Continue until clean or max iterations (3)

```bash
# Check iteration count from lifecycle
# If issues and iteration < max_iterations, loop back to execute
python3 .plan/execute-script.py pm-workflow:plan-marshall:manage-lifecycle set-phase \
  --plan-id {plan_id} --phase 5-execute
```

### Step 5: Sonar Roundtrip (if configured)

If Sonar integration is enabled:

```
Skill: pm-workflow:workflow-integration-sonar
```

Handles Sonar quality gate and issue resolution. On findings, follows same loop-back pattern as Step 4.

### Step 6: Knowledge Capture (Advisory)

```
Skill: plan-marshall:manage-memories
```

Records any significant patterns discovered during implementation. Advisory only—does not block.

### Step 7: Lessons Capture (Advisory)

```
Skill: plan-marshall:manage-lessons
```

Records lessons learned from the implementation. Advisory only—does not block.

### Step 8: Mark Plan Complete

Transition to complete:

```bash
python3 .plan/execute-script.py pm-workflow:plan-marshall:manage-lifecycle transition \
  --plan-id {plan_id} \
  --completed 7-finalize
```

### Step 9: Log Completion

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO "[STATUS] (pm-workflow:phase-7-finalize) Plan completed: commit={commit_hash}, PR={pr_url|skipped}"
```

---

## Output

**Success**:

```toon
status: success
plan_id: {plan_id}

actions:
  commit: {commit_hash}
  push: success
  pr: {created #{number}|skipped}
  automated_review: {completed|skipped|loop_back}
  sonar: {passed|skipped|loop_back}
  knowledge_capture: done
  lessons_capture: done

next_state: complete
```

**Loop Back** (PR issues found, iteration < 3):

```toon
status: loop_back
plan_id: {plan_id}
iteration: {current_iteration}
reason: {ci_failure|review_comments|sonar_issues}
next_phase: 5-execute
fix_tasks_created: {count}
```

**Error**:

```toon
status: error
plan_id: {plan_id}
step: {commit|push|pr|automated_review|sonar}
message: {error_description}
recovery: {recovery_suggestion}
```

---

## Error Handling

On any error, **first log the error** to work-log:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} ERROR "[ERROR] (pm-workflow:phase-7-finalize) {step} failed - {error_type}: {error_context}"
```

### Git Commit Failure

```toon
status: error
step: commit
message: Nothing to commit or merge conflict
recovery: Resolve conflicts, then re-run finalize
```

### Push Failure

```toon
status: error
step: push
message: Remote rejected push
recovery: Pull changes, resolve conflicts, then re-run finalize
```

### PR Creation Failure

```toon
status: error
step: pr
message: PR already exists or branch not pushed
recovery: Check existing PRs or push branch first
```

### Max Iterations Reached

```toon
status: error
step: iteration_limit
message: Max finalize iterations (3) reached
recovery: Manual intervention required - review remaining PR issues
```

---

## Resumability

The skill checks current state before each step:

1. **Are there uncommitted changes?** Skip commit if clean
2. **Is branch pushed?** Skip push if remote is current
3. **Does PR exist?** Skip creation if PR exists
4. **Is automated review complete?** Skip if already processed
5. **Is Sonar roundtrip complete?** Skip if already processed
6. **Is plan already complete?** Skip if finalize done

---

## Shipping Pipeline

```
┌─────────────────────────────────────────────────────────┐
│                  FINALIZE PIPELINE                       │
│                                                          │
│  ┌─────────┐   ┌──────┐   ┌──────┐                      │
│  │ commit  │ → │ push │ → │  PR  │                      │
│  └─────────┘   └──────┘   └──┬───┘                      │
│                              │                           │
│                              ↓                           │
│  ┌───────────────────────────────────────────────┐      │
│  │            AUTOMATED REVIEW                    │      │
│  │  CI checks │ review comments │ Sonar gate     │      │
│  └───────────────────┬───────────────────────────┘      │
│                      │                                   │
│          ┌──────────┴──────────┐                        │
│          ↓                     ↓                        │
│      [issues]            [no issues]                    │
│          │                     │                        │
│          ↓                     ↓                        │
│   create fix tasks       COMPLETE                       │
│   loop → 5-execute                                       │
│   (max 3 iterations)                                    │
└─────────────────────────────────────────────────────────┘
```

---

## Standards (Load On-Demand)

### Validation
```
Read standards/validation.md
```
Contains: Configuration requirements, step-by-step validation checklist, output format examples

### Lessons Integration
```
Read standards/lessons-integration.md
```
Contains: How lessons are captured at plan completion, knowledge extraction patterns

---

## Templates

| Template | Purpose |
|----------|---------|
| `templates/pr-template.md` | PR body format |

---

## Integration

### Phase Routing

This skill is invoked when plan is in `7-finalize` phase:

```
pm-workflow:plan-marshall:manage-lifecycle route --phase 7-finalize → pm-workflow:phase-7-finalize
```

### Loop-Back to Execute

On PR issues (CI failures, review comments, Sonar findings):
1. Create fix tasks via `pm-workflow:manage-tasks`
2. Increment `finalize_iteration` counter
3. Transition to `5-execute` phase
4. Fix tasks run, then re-verify (6-verify), then return to `7-finalize`
5. Repeat until clean or max iterations (3)

### Command Integration

- **/plan-marshall action=finalize** - Invokes this skill
- **/pr-doctor** - Used during automated review step

### Related Skills

| Skill | Purpose |
|-------|---------|
| `pm-workflow:workflow-integration-git` | Commit, push, PR creation |
| `pm-workflow:workflow-integration-ci` | CI monitoring, review handling |
| `pm-workflow:workflow-integration-sonar` | Sonar quality gate |
| `pm-workflow:phase-6-verify` | Loop-back target for fix verification |
| `pm-workflow:plan-marshall` | Phase transitions (manage-lifecycle script) |
| `plan-marshall:manage-memories` | Knowledge capture |
| `plan-marshall:manage-lessons` | Lessons capture |
