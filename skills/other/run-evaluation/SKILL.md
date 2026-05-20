---
name: run-evaluation
description: Evaluate the latest Universal Agent run for errors, bottlenecks, and opportunities for improvement. This skill should be used after an agent run completes to perform a critical assessment by analyzing the run.log file, session directory output, and Logfire traces. Use when the user wants to debug issues, understand performance problems, identify exceptions, check if the agent stayed on a happy path, or get recommendations for improving agent behavior.
---

# Run Evaluation Skill

Perform a comprehensive post-mortem analysis of the latest Universal Agent run.

## Workflow

### Step 1: Identify the Latest Session

Find the most recent session directory:
```bash
ls -lt /home/kjdragan/lrepos/universal_agent/AGENT_RUN_WORKSPACES/ | grep session_ | head -1
```

Extract the session path (e.g., `/home/kjdragan/lrepos/universal_agent/AGENT_RUN_WORKSPACES/session_20260115_094820`).

### Step 2: Read the Run Log

Load the full run log for context:
```bash
cat {session_dir}/run.log
```

This contains the complete terminal output including:
- Tool calls and responses
- Error messages
- Timing information
- Agent decisions

### Step 3: Extract Key Metrics from run.log

Parse the log for:
- **Tool call count**: Count occurrences of `🔧 [` 
- **Error indicators**: Search for `Error`, `Failed`, `Exception`, `❌`
- **Timing**: Look at `+Xs` timestamps for latency
- **Retries/deduplication**: Search for `Idempotent`, `retry`, `deduped`

### Step 4: Query Logfire for Trace Analysis

Use the Logfire MCP tools to analyze the run. Get the trace_id from the run.log (appears near the top).

**Key queries:**

1. **Find all exceptions in the run:**
```sql
SELECT start_timestamp, span_name, exception_type, exception_message 
FROM records 
WHERE is_exception = true 
ORDER BY start_timestamp DESC
```

2. **Find slowest operations:**
```sql
SELECT span_name, duration, message 
FROM records 
WHERE duration IS NOT NULL 
ORDER BY duration DESC 
LIMIT 20
```

3. **Find tool execution timeline:**
```sql
SELECT start_timestamp, span_name, duration, message 
FROM records 
WHERE span_name LIKE '%tool%' OR message LIKE '%Tool%' 
ORDER BY start_timestamp
```

4. **Find warnings and errors:**
```sql
SELECT start_timestamp, message, level, exception_message 
FROM records 
WHERE level >= 30 
ORDER BY start_timestamp
```

### Step 5: Analyze Session Artifacts

Check the session directory structure:
```bash
find {session_dir} -type f -name "*.md" -o -name "*.json" -o -name "*.html" | head -30
```

Verify expected outputs exist:
- `tasks/{task_name}/refined_corpus.md` - Research corpus
- `work_products/*.html` - Final report
- `search_results/` - Search result JSON files (may be archived)

### Step 6: Generate Evaluation Report

Produce a structured report with these sections:

## Evaluation Report Template

```markdown
# Agent Run Evaluation Report

**Session:** {session_dir}
**Timestamp:** {datetime}
**Total Duration:** {total_time}

## Executive Summary
[1-2 sentence overall assessment]

## Metrics Overview
| Metric | Value | Status |
|--------|-------|--------|
| Total Tool Calls | X | ✅/⚠️/❌ |
| Exceptions | X | ✅/⚠️/❌ |
| Average Tool Latency | Xs | ✅/⚠️/❌ |
| Retries/Dedupes | X | ✅/⚠️/❌ |

## Happy Path Analysis
- [Did the agent follow the expected workflow?]
- [Were there any unexpected detours?]
- [Did sub-agents complete their tasks?]

## Exceptions & Errors
[List each exception with context and potential cause]

## Performance Bottlenecks
[List slowest operations and why they were slow]

## Opportunities for Improvement
1. [Specific actionable recommendation]
2. [Specific actionable recommendation]
3. [Specific actionable recommendation]

## Logfire Trace Links
- [Link to full trace in Logfire UI]
```

## Evaluation Criteria

### Happy Path Indicators (✅)
- Sub-agents return successfully
- No more than 1 retry per tool
- finalize_research finds search results
- Report written to work_products/
- Email sent successfully

### Warning Indicators (⚠️)
- Tool retries (2-3 attempts)
- Idempotency guard triggered
- Long latencies (>60s per tool)
- Missing expected files

### Critical Indicators (❌)
- Exceptions raised
- Tool returning `None`
- Infinite loop detection
- Budget exceeded
- HarnessError raised

## Output

Write the evaluation report to:
```
{session_dir}/run_evaluation.md
```
