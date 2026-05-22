---
name: testing-dags
description: Complex DAG testing workflows with debugging and fixing cycles. Use for multi-step testing requests like "test this dag and fix it if it fails", "test and debug", "run the pipeline and troubleshoot issues". For simple test requests ("test dag", "run dag"), the airflow entrypoint skill handles it directly. This skill is for iterative test-debug-fix cycles.
---

# DAG Testing Skill

---

## 🚀 FIRST ACTION: Just Trigger the DAG

When the user asks to test a DAG, your **FIRST AND ONLY action** should be:

```
trigger_dag_and_wait(dag_id="<dag_id>", timeout=300)
```

**DO NOT:**
- ❌ Call `list_dags` first
- ❌ Call `get_dag_details` first
- ❌ Call `list_import_errors` first
- ❌ Use `grep` or `ls` or any bash command
- ❌ Do any "pre-flight checks"

**Just trigger the DAG.** If it fails, THEN debug.

---

## ⚠️ CRITICAL WARNING: Use MCP Tools, NOT CLI Commands ⚠️

> **STOP! Before running ANY Airflow-related command, read this.**
>
> You MUST use MCP tools for ALL Airflow interactions. CLI commands like `astro dev run`, `airflow dags test`, or shell commands to read logs are **FORBIDDEN**.
>
> **Why?** MCP tools provide structured, reliable output. CLI commands are fragile, produce unstructured text, and often fail silently.

---

## CLI vs MCP Quick Reference

| ❌ DO NOT USE | ✅ USE INSTEAD |
|---------------|----------------|
| `astro dev run dags test` | `trigger_dag_and_wait` MCP tool |
| `airflow dags test` | `trigger_dag_and_wait` MCP tool |
| `airflow tasks test` | `trigger_dag_and_wait` MCP tool |
| `cat` / `grep` / `tail` on logs | `get_task_logs` MCP tool |
| `astro dev run dags list` | `list_dags` MCP tool |
| Any `astro dev run ...` | Equivalent MCP tool |
| Any `airflow ...` CLI | Equivalent MCP tool |
| `ls` on `/usr/local/airflow/dags/` | `list_dags` or `explore_dag` MCP tool |
| `cat ... \| jq` to filter MCP results | Read the JSON directly from MCP response |
| `grep` on MCP tool result files | Read the JSON directly from MCP response |
| `ls` on local dags directory | Not needed — just trigger the DAG |
| `pwd` to check directory | Not needed — just trigger the DAG |

**Remember:**
- ✅ Airflow is ALREADY running — the MCP server handles the connection
- ✅ Just call `trigger_dag_and_wait` — don't check anything first
- ❌ Do NOT call `list_dags` before testing — just trigger
- ❌ Do NOT use shell commands (`ls`, `grep`, `cat`, `pwd`)
- ❌ Do NOT use bash to parse or filter MCP tool results
- ❌ Do NOT do "pre-flight checks" — try first, debug on failure

---

## Testing Workflow Overview

```
┌─────────────────────────────────────┐
│ 1. TRIGGER AND WAIT                 │
│    Run DAG, wait for completion     │
└─────────────────────────────────────┘
                 ↓
        ┌───────┴───────┐
        ↓               ↓
   ┌─────────┐    ┌──────────┐
   │ SUCCESS │    │ FAILED   │
   │ Done!   │    │ Debug... │
   └─────────┘    └──────────┘
                       ↓
        ┌─────────────────────────────────────┐
        │ 2. DEBUG (only if failed)           │
        │    Get logs, identify root cause    │
        └─────────────────────────────────────┘
                       ↓
        ┌─────────────────────────────────────┐
        │ 3. FIX AND RETEST                   │
        │    Apply fix, restart from step 1   │
        └─────────────────────────────────────┘
```

**Philosophy: Try first, debug on failure.** Don't waste time on pre-flight checks — just run the DAG and diagnose if something goes wrong.

---

## Phase 1: Trigger and Wait

Use `trigger_dag_and_wait` to test the DAG:

### Primary Method: Trigger and Wait

**MCP tool:** `trigger_dag_and_wait(dag_id="your_dag_id", timeout=300)`

```
trigger_dag_and_wait(
    dag_id="my_dag",
    conf={},           # Optional: pass config to the DAG
    timeout=300        # Wait up to 5 minutes (adjust as needed)
)
```

**Why this is the preferred method:**
- Single tool call handles trigger + monitoring
- Returns immediately when DAG completes (success or failure)
- Includes failed task details if run fails
- No manual polling required

### Response Interpretation

**Success:**
```json
{
  "dag_run": {
    "dag_id": "my_dag",
    "dag_run_id": "manual__2025-01-14T...",
    "state": "success",
    "start_date": "...",
    "end_date": "..."
  },
  "timed_out": false,
  "elapsed_seconds": 45.2
}
```

**Failure:**
```json
{
  "dag_run": {
    "state": "failed"
  },
  "timed_out": false,
  "elapsed_seconds": 30.1,
  "failed_tasks": [
    {
      "task_id": "extract_data",
      "state": "failed",
      "try_number": 2
    }
  ]
}
```

**Timeout:**
```json
{
  "dag_id": "my_dag",
  "dag_run_id": "manual__...",
  "state": "running",
  "timed_out": true,
  "elapsed_seconds": 300.0,
  "message": "Timed out after 300 seconds. DAG run is still running."
}
```

### Alternative: Trigger and Monitor Separately

Use this only when you need more control:

```
# Step 1: Trigger
trigger_dag(dag_id="my_dag", conf={})
# Returns: {"dag_run_id": "manual__...", "state": "queued"}

# Step 2: Check status
get_dag_run(dag_id="my_dag", dag_run_id="manual__...")
# Returns current state
```

---

## Handling Results

### If Success

The DAG ran successfully. Summarize for the user:
- Total elapsed time
- Number of tasks completed
- Any notable outputs (if visible in logs)

**You're done!**

### If Timed Out

The DAG is still running. Options:
1. Check current status with `get_dag_run(dag_id, dag_run_id)`
2. Ask user if they want to continue waiting
3. Increase timeout and try again

### If Failed

Move to Phase 2 (Debug) to identify the root cause.

---

## Phase 2: Debug Failures (Only If Needed)

When a DAG run fails, use these tools to diagnose:

### Get Comprehensive Diagnosis

**MCP tool:** `diagnose_dag_run(dag_id, dag_run_id)`

Returns in one call:
- Run metadata (state, timing)
- All task instances with states
- Summary of failed tasks
- State counts (success, failed, skipped, etc.)

### Get Task Logs

**MCP tool:** `get_task_logs(dag_id, dag_run_id, task_id)`

```
get_task_logs(
    dag_id="my_dag",
    dag_run_id="manual__2025-01-14T...",
    task_id="extract_data",
    try_number=1        # Which attempt (1 = first try)
)
```

**Look for:**
- Exception messages and stack traces
- Connection errors (database, API, S3)
- Permission errors
- Timeout errors
- Missing dependencies

### Check Upstream Tasks

If a task shows `upstream_failed`, the root cause is in an upstream task. Use `diagnose_dag_run` to find which task actually failed.

### Check Import Errors (If DAG Didn't Run)

If the trigger failed because the DAG doesn't exist:

**MCP tool:** `list_import_errors`

This reveals syntax errors or missing dependencies that prevented the DAG from loading.

---

## Phase 3: Fix and Retest

Once you identify the issue:

### Common Fixes

| Issue | Fix |
|-------|-----|
| Missing import | Add to DAG file |
| Missing package | Add to `requirements.txt` |
| Connection error | Check `list_connections`, verify credentials |
| Variable missing | Check `list_variables`, create if needed |
| Timeout | Increase task timeout or optimize query |
| Permission error | Check credentials in connection |

### After Fixing

1. Save the file
2. **Retest:** `trigger_dag_and_wait(dag_id)`

**Repeat the test → debug → fix loop until the DAG succeeds.**

---

## MCP Tools Quick Reference

| Phase | Tool | Purpose |
|-------|------|---------|
| Test | `trigger_dag_and_wait` | **Primary test method — start here** |
| Test | `trigger_dag` | Start run (alternative) |
| Test | `get_dag_run` | Check run status |
| Debug | `diagnose_dag_run` | Comprehensive failure diagnosis |
| Debug | `get_task_logs` | Get task output/errors |
| Debug | `list_import_errors` | Check for parse errors (if DAG won't load) |
| Debug | `get_dag_details` | Verify DAG config |
| Debug | `explore_dag` | Full DAG inspection |

---

## Testing Scenarios

### Scenario 1: Test a DAG (Happy Path)

```
1. trigger_dag_and_wait(dag_id) → Run and wait
2. Success! Done.
```

### Scenario 2: Test a DAG (With Failure)

```
1. trigger_dag_and_wait(dag_id) → Run and wait
2. Failed → diagnose_dag_run    → Find failed tasks
3. get_task_logs                → Get error details
4. [Fix the issue]
5. trigger_dag_and_wait(dag_id) → Retest
```

### Scenario 3: DAG Doesn't Exist / Won't Load

```
1. trigger_dag_and_wait(dag_id) → Error: DAG not found
2. list_import_errors           → Find parse error
3. [Fix the issue]
4. trigger_dag_and_wait(dag_id) → Retest
```

### Scenario 4: Debug a Failed Scheduled Run

```
1. diagnose_dag_run(dag_id, dag_run_id)  → Get failure summary
2. get_task_logs(dag_id, dag_run_id, failed_task_id) → Get error
3. [Fix the issue]
4. trigger_dag_and_wait(dag_id)          → Retest
```

### Scenario 5: Test with Custom Configuration

```
1. trigger_dag_and_wait(
       dag_id="my_dag",
       conf={"env": "staging", "batch_size": 100},
       timeout=600
   )
2. [Analyze results]
```

### Scenario 6: Long-Running DAG

```
1. trigger_dag_and_wait(dag_id, timeout=3600)  → Wait up to 1 hour
2. [If timed out] get_dag_run(dag_id, dag_run_id) → Check current state
```

---

## Debugging Tips

### Common Error Patterns

**Connection Refused / Timeout:**
- Check `list_connections` for correct host/port
- Verify network connectivity to external system
- Check if connection credentials are correct

**ModuleNotFoundError:**
- Package missing from `requirements.txt`
- After adding, may need environment restart

**PermissionError:**
- Check IAM roles, database grants, API keys
- Verify connection has correct credentials

**Task Timeout:**
- Query or operation taking too long
- Consider adding timeout parameter to task
- Optimize underlying query/operation

### Reading Task Logs

Task logs typically show:
1. Task start timestamp
2. Any print/log statements from task code
3. Return value (for @task decorated functions)
4. Exception + full stack trace (if failed)
5. Task end timestamp and duration

**Focus on the exception at the bottom of failed task logs.**

---

## Related Skills

- **authoring-dags**: For creating new DAGs (includes validation before testing)
- **debugging-dags**: For general Airflow troubleshooting
