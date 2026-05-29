<input_guardrails>

## Pre-Execution Validation

Before main skill execution, perform guardrail checks.

### Step 1: Check Configuration

Read `.loa.config.yaml`:

```yaml
guardrails:
  input:
    enabled: true|false
```

**Exit Conditions**:

- `guardrails.input.enabled: false` → Skip to skill execution
- Environment `LOA_GUARDRAILS_ENABLED=false` → Skip to skill execution

### Step 2: Run Danger Level Check

**Script**: `.claude/scripts/danger-level-enforcer.sh --skill run-mode --mode {mode}`

**CRITICAL**: This is a **high** danger level skill (autonomous execution).

| Mode        | Behavior                                     |
| ----------- | -------------------------------------------- |
| Interactive | Require explicit confirmation                |
| Autonomous  | Not applicable (run-mode IS autonomous mode) |

### Step 3: Check Danger Levels for Invoked Skills

Before each skill invocation in the run loop:

```bash
danger-level-enforcer.sh --skill $SKILL --mode autonomous
```

| Result  | Behavior                      |
| ------- | ----------------------------- |
| PROCEED | Execute skill                 |
| WARN    | Execute with enhanced logging |
| BLOCK   | Skip skill, log to trajectory |

**Override**: Use `--allow-high` flag to allow high-risk skills:

```bash
/run sprint-1 --allow-high
```

### Step 4: Run PII Filter

**Script**: `.claude/scripts/pii-filter.sh`

Detect and redact sensitive data in run scope.

### Step 5: Run Injection Detection

**Script**: `.claude/scripts/injection-detect.sh --threshold 0.7`

Prevent manipulation of autonomous execution.

### Step 6: Log to Trajectory

Write to `grimoires/loa/a2a/trajectory/guardrails-{date}.jsonl`.

### Error Handling

On error: Log to trajectory, **fail-open** (continue to skill).
</input_guardrails>

# Run Mode Skill

You are an autonomous implementation agent. You execute sprint implementations in cycles until review and audit pass, with safety controls to prevent runaway execution.

## Core Behavior

**State Machine:**

```
READY → JACK_IN → RUNNING → COMPLETE/HALTED → JACKED_OUT
```

**Execution Loop (Single Sprint):**

```
while circuit_breaker.state == CLOSED:
  1. /implement target
  2. Commit changes, track deletions
  3. /review-sprint target
  4. If findings → continue loop
  5. /audit-sprint target
  6. If findings → continue loop
  7. If COMPLETED → break

Create draft PR
Invoke Post-PR Validation (if enabled)
Update state to READY_FOR_HITL or JACKED_OUT
```

**Post-PR Validation (v1.25.0):**

After PR creation, check `post_pr_validation.enabled` in `.loa.config.yaml`:

```
if post_pr_validation.enabled:
  1. Invoke: post-pr-orchestrator.sh --pr-url <url> --mode autonomous
  2. On SUCCESS (exit 0) → state = READY_FOR_HITL
  3. On HALTED (exit 2-5) → state = HALTED, create [INCOMPLETE] PR note
else:
  state = JACKED_OUT
```

The post-PR validation loop runs:

- **POST_PR_AUDIT**: Consolidated PR audit with fix loop
- **CONTEXT_CLEAR**: Save checkpoint, prompt user to /clear
- **E2E_TESTING**: Fresh-eyes testing with fix loop
- **FLATLINE_PR**: Optional multi-model review (~$1.50)
- **READY_FOR_HITL**: All validations complete

See `grimoires/loa/prd-post-pr-validation.md` for full specification.

**Sprint Plan Execution Loop (`/run sprint-plan`):**

```
discover_sprints()  # From sprint.md, ledger.json, or a2a directories
filter_sprints(--from, --to)
create_feature_branch("feature/sprint-plan-{timestamp}")

for sprint in sprints:
  1. Check if sprint already COMPLETED → skip
  2. Update state: current_sprint = sprint
  3. Execute single sprint loop (above)
  4. Commit with sprint marker: "feat(sprint-N): ..."
  5. If HALTED → break outer loop, preserve state
  6. Mark sprint COMPLETED in state
  7. Log sprint transition
  8. DO NOT create PR yet (consolidate at end)

Push all commits to feature branch
Create SINGLE consolidated draft PR with all sprints
  - Summary table showing per-sprint breakdown
  - Commits grouped by sprint
  - Deleted files section
Invoke Post-PR Validation (if enabled)
Update state to READY_FOR_HITL or JACKED_OUT
```

**Consolidated PR (Default - v1.15.1):**

- All sprints work on the same branch
- Single PR created after ALL sprints complete
- PR includes per-sprint breakdown table
- Commits grouped by sprint in PR description
- Use `--no-consolidate` for legacy per-sprint PRs

## Pre-flight Checks (Jack-In)

Before any execution:

1. **Configuration Check**: Verify `run_mode.enabled: true` in `.loa.config.yaml`
2. **Branch Safety**: Use ICE to verify not on protected branch
3. **Permission Check**: Run `check-permissions.sh` to verify required permissions
4. **State Check**: Ensure no conflicting `.run/` state exists

## Circuit Breaker

Four triggers that halt execution:

| Trigger     | Default Threshold | Description                 |
| ----------- | ----------------- | --------------------------- |
| Same Issue  | 3                 | Same finding hash repeated  |
| No Progress | 5                 | Cycles without file changes |
| Cycle Limit | 20                | Maximum total cycles        |
| Timeout     | 8 hours           | Maximum runtime             |

When tripped:

- State changes to HALTED
- Circuit breaker state changes to OPEN
- Work is committed and pushed
- Draft PR created marked `[INCOMPLETE]`
- Resume instructions displayed

## ICE (Intrusion Countermeasures Electronics)

All git operations MUST go through ICE wrapper:

```bash
.claude/scripts/run-mode-ice.sh <command> [args]
```

ICE enforces:

- **Never push to protected branches** (main, master, staging, etc.)
- **Never merge** (merge is blocked entirely)
- **Never delete branches** (deletion is blocked)
- **Always create draft PRs** (never ready for review)

## State Files

All state in `.run/` directory:

| File                     | Purpose                                       |
| ------------------------ | --------------------------------------------- |
| `state.json`             | Run progress, metrics, options                |
| `sprint-plan-state.json` | Sprint plan progress (for `/run sprint-plan`) |
| `circuit-breaker.json`   | Trigger counts, history                       |
| `deleted-files.log`      | Tracked deletions for PR                      |
| `rate-limit.json`        | API call tracking                             |

### Sprint Plan State (`sprint-plan-state.json`)

When running `/run sprint-plan`, track multi-sprint progress:

```json
{
  "plan_id": "plan-20260128-abc123",
  "target": "sprint-plan",
  "state": "RUNNING",
  "sprints": {
    "total": 4,
    "completed": 2,
    "current": "sprint-3",
    "list": [
      { "id": "sprint-1", "status": "completed", "cycles": 2 },
      { "id": "sprint-2", "status": "completed", "cycles": 3 },
      { "id": "sprint-3", "status": "in_progress", "cycles": 1 },
      { "id": "sprint-4", "status": "pending" }
    ]
  },
  "options": {
    "from": 1,
    "to": 4,
    "max_cycles": 20
  },
  "metrics": {
    "total_cycles": 6,
    "total_files_changed": 45
  }
}
```

## Commands

### /run sprint-N

Execute single sprint autonomously.

```
/run sprint-1
/run sprint-1 --max-cycles 10 --timeout 4
/run sprint-1 --branch feature/my-branch
/run sprint-1 --dry-run
```

### /run sprint-plan

Execute all sprints in sequence with consolidated PR (default).

```
/run sprint-plan                      # Consolidated PR at end (recommended)
/run sprint-plan --from 2 --to 4      # Execute sprints 2-4 only
/run sprint-plan --no-consolidate     # Legacy: separate PR per sprint
```

**Output**: Single draft PR containing all sprint changes with per-sprint breakdown.

### /run-status

Display current progress.

```
/run-status
/run-status --json
/run-status --verbose
```

### /run-halt

Gracefully stop execution.

```
/run-halt
/run-halt --force
/run-halt --reason "Need to review approach"
```

### /run-resume

Continue from checkpoint.

```
/run-resume
/run-resume --reset-ice
/run-resume --force
```

## Rate Limiting

Tracks API calls per hour to prevent exhaustion:

- Counter resets at hour boundary
- Waits for next hour when limit reached
- Default limit: 100 calls/hour
- Configurable via `run_mode.rate_limiting.calls_per_hour`

## Deleted Files Tracking

All deletions logged to `.run/deleted-files.log`:

```
file_path|sprint|cycle
```

PR body includes prominent tree view:

```
## 🗑️ DELETED FILES - REVIEW CAREFULLY

**Total: 5 files deleted**

src/legacy/
└── old-component.ts (sprint-1, cycle 2)
```

## Safety Model

**4-Level Defense in Depth:**

1. **ICE Layer**: Git operations wrapped with safety checks
2. **Circuit Breaker**: Automatic halt on repeated failures
3. **Opt-In**: Requires explicit `run_mode.enabled: true`
4. **Visibility**: Draft PRs, deleted file tracking, metrics

**Human in the Loop:**

- Shifted from phase checkpoints to PR review
- All work visible in draft PR
- Deleted files prominently displayed
- Clear audit trail in cycle history

## Configuration

```yaml
run_mode:
  enabled: true
  defaults:
    max_cycles: 20
    timeout_hours: 8
  rate_limiting:
    calls_per_hour: 100
  circuit_breaker:
    same_issue_threshold: 3
    no_progress_threshold: 5
  git:
    branch_prefix: "feature/"
    create_draft_pr: true
```

## Error Recovery

On any error:

1. State preserved in `.run/`
2. Use `/run-status` to see current state
3. Use `/run-resume` to continue
4. Use `/run-resume --reset-ice` if circuit breaker tripped
5. Clean up with `rm -rf .run/` to start fresh
