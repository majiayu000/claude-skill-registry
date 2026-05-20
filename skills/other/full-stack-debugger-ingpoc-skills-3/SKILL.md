---
name: full-stack-debugger
description: This skill should be used when debugging full-stack issues that span UI, backend, and database layers. It provides a systematic workflow to detect errors, analyze root causes, apply fixes iteratively, and verify solutions through automated server restarts and browser-based testing. Ideal for scenarios like failing schedulers, import errors, database issues, or API payload problems where issues originate in backend code but manifest in the UI.
---

# Full Stack Debugger

## Overview

The Full Stack Debugger enables systematic debugging of issues across the entire application stack (UI/Frontend, Backend/API, Database/State). It combines browser testing, log analysis, code examination, and automated server restart/verification to iteratively identify and fix issues one at a time until the system is fully operational.

This skill uses a proven workflow: **Detection → Analysis → Fix → Restart → Verification → Iteration** to systematically resolve issues that developers encounter during development and testing.

## When to Use This Skill

Trigger this skill when observing:
- Error states in the UI (dashboard, buttons failing, status showing errors)
- Repeated failures in backend logs (task execution failures, import errors, database errors)
- Unexpected database state (rows showing failed status when they should succeed)
- API endpoints returning errors or unexpected responses
- Services failing to initialize or process tasks
- Cascading failures across multiple components

## Debugging Workflow

### Phase 1: Detection

Detect errors from multiple sources:

**Browser UI Detection:**
- Navigate to the affected page/feature in the browser
- Check for error messages, red warning states, or disabled functionality
- Read console error messages using DevTools
- Note the specific UI state and what action triggered the error

**Backend Log Detection:**
- Query recent error logs using `tail -200 /path/to/logs/errors.log`
- Search for error patterns related to the issue using `grep`
- Note error timestamps, error messages, and stack traces
- Look for repeated errors (indicates systemic issue)

**Database State Detection:**
- Query the database directly using sqlite3
- Check status of recent tasks, transactions, or records
- Look for failed, incomplete, or error states
- Note which records are affected and what their states are

**Example:** When debugging a scheduler failure:
1. Navigate to System Health dashboard
2. Observe scheduler showing "0 done" or "X failed"
3. Check `/logs/errors.log` for error messages
4. Query `queue_tasks` table to see failed task records

### Phase 2: Analysis

Analyze root causes by reading code and logs:

**Code Analysis:**
- Read the error file/module indicated in error stack traces
- Check imports - look for missing `from X import Y` statements
- Check class names - verify instantiation matches actual class names
- Look for syntax errors - unmatched quotes, unclosed parentheses
- Check function signatures - ensure payloads match expected parameters
- Read reference documentation (`references/common_errors.md`) for error patterns

**Log Analysis:**
- Extract error messages from logs
- Look for patterns like `'optional'` (missing import), `unterminated string` (syntax error), `'attribute'` (wrong class name)
- Trace error propagation backward to find the originating issue
- Check timestamps - multiple errors at same time indicate batch failure

**API/Payload Analysis:**
- Check what payload the API is sending to task handlers
- Read the task handler code to see what fields it expects
- Compare actual payload vs expected payload
- Look for missing required fields

**Example:** When debugging "name 'Optional' is not defined":
1. Find the file mentioned in error (`analysis_executor.py`)
2. Read the imports section
3. Notice `Optional` is used but not imported
4. Check line 14: `from typing import Dict, List, Any` - missing `Optional`
5. Fix: Add `Optional` to the import statement

### Phase 3: Fix (One Issue at a Time)

Apply fixes one issue per iteration:

**Before Fixing:**
- Verify this is the first/next issue to fix
- Read the relevant code section carefully
- Use the fix patterns from `references/fix_templates.md`

**Common Fix Patterns:**
- **Missing imports:** Add to import statement (e.g., `from typing import Optional`)
- **Wrong class name:** Update import and instantiation to match actual class
- **Missing docstring quotes:** Add opening `"""` to docstring
- **Wrong payload fields:** Add missing required fields to payload dictionary
- **Syntax errors:** Fix unmatched quotes, parentheses, brackets

**After Fixing:**
- Read back the changed code to verify syntax
- Check the edit was correct (line numbers, indentation)
- Only fix ONE issue, even if multiple exist - don't cascade fixes
- Document what was changed in a clear comment

**Example Fix:**
```python
# BEFORE
from typing import Dict, List, Any

# AFTER
from typing import Dict, List, Any, Optional
```

### Phase 4: Restart (Automated)

Restart the backend server after each fix:

```bash
# Kill existing processes
lsof -ti:8000 | xargs kill -9 2>/dev/null

# Clear Python bytecode cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

# Restart backend
sleep 3 && python -m src.main --command web > /tmp/backend_restart.log 2>&1 &
sleep 10  # Wait for startup

# Verify health
curl -m 5 http://localhost:8000/api/health
```

### Phase 5: Verification

Verify the fix worked through multiple checks:

**Health Check:**
- Call `/api/health` endpoint
- Verify `"status": "healthy"`
- If still failing, check logs for new errors

**Browser Verification:**
- Navigate to the affected UI page
- Trigger the action that previously failed
- Verify the error is gone
- Check for new errors in console

**Database Verification:**
- Query the affected records/tasks
- Verify status changed from failed/error to success/completed
- Check that metrics updated (e.g., scheduler shows "1 done" instead of "0 done")

**Log Verification:**
- Check recent logs for the same error
- Verify no new errors appeared
- Look for success messages or "completed" status

**Example:**
- Scheduler should show "1 done" instead of "0 done"
- Task record should show status="completed" instead of "failed"
- No error messages in logs
- WebSocket shows healthy status in UI

### Phase 6: Iteration

If issues remain, repeat the cycle:

1. **Continue if more issues exist:**
   - Check logs for remaining errors
   - If yes, return to Phase 2 (Analysis)
   - Fix the next issue (Phase 3)
   - Restart (Phase 4)
   - Verify (Phase 5)

2. **Stop when all issues fixed:**
   - All schedulers show completed execution counts
   - UI shows no error states
   - Logs show no error patterns
   - Tasks/records show success status
   - Full verification complete

## Common Error Patterns

See `references/common_errors.md` for patterns to recognize:
- Python syntax errors (unterminated strings, missing quotes)
- Import errors (`name 'X' is not defined`, `cannot import name 'Y'`)
- Class/attribute errors (`'dict' object has no attribute 'symbol'`)
- Type errors (passing wrong data type)
- Payload/configuration errors (missing required fields)

## Fix Templates

See `references/fix_templates.md` for ready-to-use fix patterns:
- How to add missing imports
- How to fix class name mismatches
- How to fix docstring syntax
- How to add missing payload fields
- How to fix type errors

## Tools Used

- **Playwright Browser Tools:** Navigate UI, verify changes
- **Read/Grep Tools:** Examine code and logs
- **Bash:** Server restart, cache clearing, health checks
- **Edit Tool:** Apply code fixes
- **Database Queries:** Verify task/record state

## MCP Tools Integration

Use robo-trader-dev MCP tools for 95%+ token-efficient debugging:

| Task | MCP Tool | Token Savings | Usage |
|------|----------|---------------|-------|
| Analyze error logs | `mcp__robo-trader-dev__analyze_logs` | 98% | Pattern detection with time windows |
| System health check | `mcp__robo-trader-dev__check_system_health` | 97% | Database, queues, API, disk status |
| Diagnose DB locks | `mcp__robo-trader-dev__diagnose_database_locks` | 95% | Correlate logs with code patterns |
| Queue monitoring | `mcp__robo-trader-dev__queue_status` | 96% | Real-time queue backlog analysis |
| Coordinator status | `mcp__robo-trader-dev__coordinator_status` | 94% | Init status, error details |
| Error pattern fix | `mcp__robo-trader-dev__suggest_fix` | 90% | Known pattern matching with examples |
| Read code files | `mcp__robo-trader-dev__smart_file_read` | 85% | Progressive context (summary/targeted/full) |
| Find related files | `mcp__robo-trader-dev__find_related_files` | 88% | Import/git/similarity analysis |

**Example debugging workflow**:
```python
# 1. Detect errors (MCP instead of tail/grep)
mcp__robo-trader-dev__analyze_logs(patterns=["ERROR", "TIMEOUT"], time_window="1h")

# 2. Check system health (MCP instead of curl loops)
mcp__robo-trader-dev__check_system_health(components=["database", "queues", "api_endpoints"])

# 3. Diagnose specific issue (MCP instead of sqlite3 + code reading)
mcp__robo-trader-dev__diagnose_database_locks(time_window="24h", include_code_references=True)

# 4. Get fix suggestions (MCP instead of manual pattern matching)
mcp__robo-trader-dev__suggest_fix(error_message="name 'Optional' is not defined", context_file="src/services/analyzer.py")
```

**Integration with robo-trader architecture**:
- Queue operations: Use `queue_status` to monitor PORTFOLIO_SYNC, DATA_FETCHER, AI_ANALYSIS
- Coordinator debugging: Use `coordinator_status` for BroadcastCoordinator, AIChatCoordinator init issues
- Database access: Use `query_portfolio` or `diagnose_database_locks` instead of direct sqlite3 connections

## Key Principles

1. **One issue at a time** - Fix one problem per iteration to prevent cascading failures
2. **Verify immediately** - Always restart and verify after each fix
3. **Multi-layer detection** - Check UI, logs, and database for clues
4. **Iterative refinement** - Continue until all issues resolved
5. **Automated restart** - Always use clean restart (kill + cache clear + restart)
6. **Browser verification** - Always test in actual UI, not just logs

