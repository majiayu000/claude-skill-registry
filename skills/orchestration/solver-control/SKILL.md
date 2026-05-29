---
name: solver-control
description: Solver kill-switch and progress monitoring for schedule generation. Use when aborting runaway solvers, monitoring long-running schedule generation, or integrating abort checks into solver loops.
model_tier: sonnet
parallel_hints:
  can_parallel_with: [resilience-dashboard, schedule-validator]
  must_serialize_with: [safe-schedule-generation, SCHEDULING]
  preferred_batch_size: 1
context_hints:
  max_file_context: 20
  compression_level: 1
  requires_git_context: false
  requires_db_context: true
escalation_triggers:
  - pattern: "force.*kill"
    reason: "Force killing may cause data corruption - requires human approval"
  - pattern: "emergency.*stop"
    reason: "Emergency operations require human oversight"
  - keyword: ["production", "live"]
    reason: "Production system operations require human approval"
---

# Solver Control (Kill-Switch & Progress Monitoring)

Operational control for schedule generation solvers. Enables graceful abort of runaway jobs and real-time progress monitoring.

## When This Skill Activates

- Solver is taking too long and needs to be stopped
- Monitoring progress of a long-running schedule generation
- Integrating abort checks into solver code
- Debugging solver performance or stuck jobs
- Emergency situations requiring immediate solver termination

## Quick Reference

### Abort a Running Solver

```bash
# Via API (requires auth token)
curl -X POST http://localhost:8000/scheduler/runs/{run_id}/abort \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason": "taking too long", "requested_by": "admin"}'
```

### Check Solver Progress

```bash
# Get progress for specific run
curl http://localhost:8000/scheduler/runs/{run_id}/progress \
  -H "Authorization: Bearer $TOKEN"

# List all active solver runs
curl http://localhost:8000/scheduler/runs/active \
  -H "Authorization: Bearer $TOKEN"
```

### Redis Direct (Emergency)

```bash
# Set abort flag directly in Redis
docker-compose exec redis redis-cli SET "solver:abort:{run_id}" '{"reason":"emergency","requested_by":"ops"}'

# Check if abort flag is set
docker-compose exec redis redis-cli GET "solver:abort:{run_id}"

# Check solver progress
docker-compose exec redis redis-cli HGETALL "solver:progress:{run_id}"
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/scheduler/runs/{run_id}/abort` | POST | Signal solver to abort gracefully |
| `/scheduler/runs/{run_id}/progress` | GET | Get current solver progress |
| `/scheduler/runs/active` | GET | List all active solver runs |

## Key Files

| File | Purpose |
|------|---------|
| `backend/app/scheduling/solver_control.py` | Core SolverControl class |
| `backend/app/api/routes/scheduler_ops.py` | API endpoints |
| `backend/app/schemas/scheduler_ops.py` | Request/response schemas |

## Integrating Abort Checks into Solvers

### Basic Integration Pattern

```python
from app.scheduling.solver_control import SolverControl

def solve_with_abort_support(context, run_id: str):
    """Solver that checks for abort signals."""
    best_solution = None

    for iteration in range(max_iterations):
        # CHECK FOR ABORT - do this every iteration
        if abort_reason := SolverControl.should_abort(run_id):
            # Save partial result before stopping
            SolverControl.save_partial_result(
                run_id, best_solution, best_score, abort_reason
            )
            SolverControl.clear_abort(run_id)
            raise RuntimeError(f"Solver aborted: {abort_reason}")

        # Update progress for monitoring
        SolverControl.update_progress(
            run_id=run_id,
            iteration=iteration,
            best_score=current_score,
            assignments_count=len(current_assignments),
            violations_count=violation_count,
            status="running"
        )

        # ... actual solver logic ...

        if new_solution_better:
            best_solution = current_solution

    # Mark as completed
    SolverControl.update_progress(run_id, iteration, best_score,
                                   len(best_solution), 0, "completed")
    return best_solution
```

### CP-SAT Integration (Solution Callback)

```python
from ortools.sat.python import cp_model
from app.scheduling.solver_control import SolverControl

class AbortableSolutionCallback(cp_model.CpSolverSolutionCallback):
    """CP-SAT callback that checks for abort signals."""

    def __init__(self, run_id: str, variables: dict):
        super().__init__()
        self.run_id = run_id
        self.variables = variables
        self.solution_count = 0
        self.best_solution = None

    def on_solution_callback(self):
        self.solution_count += 1

        # Check for abort signal
        if abort_reason := SolverControl.should_abort(self.run_id):
            self.StopSearch()
            return

        # Update progress
        SolverControl.update_progress(
            run_id=self.run_id,
            iteration=self.solution_count,
            best_score=self.ObjectiveValue(),
            assignments_count=self._count_assignments(),
            status="running"
        )

        # Store best solution
        self.best_solution = self._extract_solution()
```

### Greedy Solver Integration

```python
from app.scheduling.solver_control import SolverControl

class GreedySolver(BaseSolver):
    def solve(self, context, run_id: str = None):
        assignments = []

        for block in context.blocks:
            # Check abort every N blocks to avoid overhead
            if run_id and len(assignments) % 10 == 0:
                if SolverControl.should_abort(run_id):
                    return PartialResult(assignments, aborted=True)

                SolverControl.update_progress(
                    run_id, len(assignments), self._score(assignments),
                    len(assignments), 0, "running"
                )

            # ... assign block ...

        return SolverResult(assignments)
```

## SolverControl API Reference

```python
from app.scheduling.solver_control import SolverControl

# Request abort (from API or operator)
SolverControl.request_abort(
    run_id="schedule-run-123",
    reason="taking too long",
    requested_by="admin"
)

# Check if should abort (call in solver loop)
if reason := SolverControl.should_abort("schedule-run-123"):
    # Handle abort
    pass

# Update progress (call periodically in solver)
SolverControl.update_progress(
    run_id="schedule-run-123",
    iteration=1500,
    best_score=0.85,
    assignments_count=150,
    violations_count=2,
    status="running"  # or "completing", "aborted"
)

# Get progress (for monitoring)
progress = SolverControl.get_progress("schedule-run-123")
# Returns: {run_id, iteration, best_score, assignments_count, violations_count, status, updated_at}

# Save partial result when interrupted
SolverControl.save_partial_result(
    run_id="schedule-run-123",
    assignments=best_assignments_so_far,
    score=0.85,
    reason="abort_requested"
)

# Clear abort flag after handling
SolverControl.clear_abort("schedule-run-123")

# Get all active runs
active = SolverControl.get_active_runs()
```

## Redis Key Structure

| Key Pattern | Type | TTL | Purpose |
|-------------|------|-----|---------|
| `solver:abort:{run_id}` | String (JSON) | 1 hour | Abort signal with reason |
| `solver:progress:{run_id}` | Hash | 2 hours | Current progress data |
| `solver:result:{run_id}` | String (JSON) | 24 hours | Partial/final results |

## Metrics Integration

When recording solver events, use the metrics helpers:

```python
from app.core.metrics.prometheus import get_metrics

metrics = get_metrics()

# Record solver iteration
metrics.record_solver_iteration("cp_sat", count=100)

# Record abort event
metrics.record_solver_abort("operator_request")  # or "timeout", "memory_limit", "error"

# Update best score during solving
metrics.update_solver_best_score("run-123", "cp_sat", 0.85)
```

## Examples

### Example 1: Monitoring Long-Running Solver

**User Request:** "The schedule generation has been running for 10 minutes. Can you check if it's making progress?"

**Claude Response:**

**Step 1: Check active solver runs**
```bash
Checking active solvers...

Active run found:
- run_id: schedule-20260312-143022
- algorithm: cp_sat
- started: 2026-03-12 14:30:22 (10 minutes ago)
- status: running
```

**Step 2: Get progress details**
```json
{
  "run_id": "schedule-20260312-143022",
  "iteration": 1847,
  "best_score": 0.82,
  "assignments_count": 1203,
  "violations_count": 5,
  "status": "running",
  "updated_at": "2026-03-12 14:39:45"
}
```

**Analysis:**
```
✅ Solver is making progress (last update 15 seconds ago)
✅ Found feasible solution (score: 0.82, 5 violations)
⚠️  Still optimizing - considering letting it run another 5 minutes

Current quality: 82% optimal with 5 ACGME violations remaining
```

**Recommendation:**
> "Solver is actively improving the schedule. Suggest waiting 5 more minutes for better optimization. I can abort now if you need the current solution (82% quality)."

### Example 2: Aborting Stuck Solver

**User Request:** "The solver has been stuck at the same score for 30 minutes. Please stop it."

**Claude Response:**

**Step 1: Verify stuck status**
```
Current progress:
- Iteration: 2453 (same as 30 min ago)
- Best score: 0.76 (no improvement)
- Last update: 28 minutes ago

⚠️  Confirmed: Solver appears stuck
```

**Step 2: Request abort**
```bash
Sending abort signal to run schedule-20260312-140000...

POST /scheduler/runs/schedule-20260312-140000/abort
{
  "reason": "No improvement for 30 minutes, score stuck at 0.76",
  "requested_by": "claude-agent"
}
```

**Step 3: Wait for graceful shutdown**
```
Abort signal sent. Waiting for solver to save partial results...
⏳ Checking status every 5 seconds...

✅ Solver stopped gracefully after 12 seconds
```

**Step 4: Report results**
```json
{
  "status": "aborted",
  "final_score": 0.76,
  "assignments_saved": 1156,
  "violations": 8,
  "reason": "No improvement for 30 minutes, score stuck at 0.76"
}
```

> "Solver stopped successfully. Saved partial solution with 1156 assignments (76% optimal, 8 violations). You can use this solution or try regenerating with adjusted constraints."

### Example 3: Emergency Stop During Deployment

**User Request:** "EMERGENCY: Stop all schedule generation immediately - we just got a deployment notification"

**Claude Response:**

**🚨 Emergency abort initiated**

**Step 1: Identify all active solvers**
```bash
Querying active solver runs...

Found 2 active runs:
1. schedule-20260312-140000 (cp_sat, 45 min runtime)
2. schedule-20260312-143500 (greedy_fallback, 2 min runtime)
```

**Step 2: Abort all in parallel**
```bash
Sending emergency abort to all active solvers...

Run 1: ✅ Abort signal sent
Run 2: ✅ Abort signal sent

Waiting for graceful shutdown (max 30 seconds)...
```

**Step 3: Monitor shutdown**
```
Run schedule-20260312-143500: ✅ Stopped (8 seconds)
Run schedule-20260312-140000: ✅ Stopped (15 seconds)

All solvers stopped successfully.
```

**Step 4: Verify clean state**
```sql
SELECT COUNT(*) FROM assignments WHERE created_at > '2026-03-12 14:00:00';
-- Result: 0 (no partial writes detected)
```

**Summary:**
```
✅ All solvers stopped
✅ No partial data in database
✅ Safe to proceed with deployment-driven schedule changes
```

> "Emergency stop complete. All schedule generation halted. Database is in clean state. Ready for manual deployment adjustments."

---

## Common CLI Scenarios

### Scenario 1: Solver Taking Too Long

```bash
# 1. Check what's running
curl http://localhost:8000/scheduler/runs/active -H "Authorization: Bearer $TOKEN"

# 2. Check progress of specific run
curl http://localhost:8000/scheduler/runs/abc123/progress -H "Authorization: Bearer $TOKEN"

# 3. If stuck, abort it
curl -X POST http://localhost:8000/scheduler/runs/abc123/abort \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"reason": "stuck at 50% for 10 minutes", "requested_by": "operator"}'
```

### Scenario 2: Emergency Stop All Solvers

```bash
# Get all active runs and abort each
for run_id in $(curl -s http://localhost:8000/scheduler/runs/active \
  -H "Authorization: Bearer $TOKEN" | jq -r '.active_runs[].run_id'); do
  curl -X POST "http://localhost:8000/scheduler/runs/$run_id/abort" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"reason": "emergency stop", "requested_by": "ops"}'
done
```

### Scenario 3: Monitoring Dashboard Query

```promql
# Solver iterations per minute by algorithm
rate(scheduler_solver_iterations_total[1m])

# Abort rate
rate(scheduler_solver_abort_total[1h])

# Best score over time (for specific run)
scheduler_solver_best_score{run_id="abc123"}
```

## Troubleshooting

### Solver Not Responding to Abort

1. **Check abort flag is set:**
   ```bash
   docker-compose exec redis redis-cli GET "solver:abort:{run_id}"
   ```

2. **Check solver is checking for abort:**
   - Ensure `SolverControl.should_abort()` is called in the solver loop
   - For CP-SAT, ensure callback has abort check in `on_solution_callback`

3. **Force kill if necessary:**
   ```bash
   # Find and kill the Celery task
   docker-compose exec backend celery -A app.core.celery_app inspect active
   docker-compose exec backend celery -A app.core.celery_app control revoke {task_id} --terminate
   ```

### Progress Not Updating

1. **Check Redis connectivity:**
   ```bash
   docker-compose exec redis redis-cli PING
   ```

2. **Check progress key:**
   ```bash
   docker-compose exec redis redis-cli HGETALL "solver:progress:{run_id}"
   ```

3. **Check solver is calling update_progress:**
   - Add logging to verify `update_progress` is being called
   - Errors in progress updates are logged at DEBUG level (won't fail solver)

## Validation Checklist

Before completing solver control operations, verify:

- [ ] **Abort Signal Set:** Abort flag is properly written to Redis for the run_id
- [ ] **Progress Updates:** Progress metrics are being updated periodically in solver loop
- [ ] **Solver Response:** Solver checks `should_abort()` at reasonable intervals (not too infrequent)
- [ ] **Partial Results Saved:** Best solution is saved before aborting (prevents lost work)
- [ ] **Cleanup Complete:** Abort flags are cleared after handling to prevent stale signals
- [ ] **Metrics Recorded:** Prometheus metrics are updated for abort/iteration events
- [ ] **No Data Corruption:** Database state is consistent (no partial writes from interrupted solver)
- [ ] **Quality Gate:** Verify Redis connectivity before critical operations

## Related Documentation

- [Scheduler Hardening TODO](docs/planning/SCHEDULER_HARDENING_TODO.md) - Future improvements
- [Solver Algorithm](docs/architecture/SOLVER_ALGORITHM.md) - Solver internals
- [Prometheus Metrics](backend/app/core/metrics/prometheus.py) - Available metrics
