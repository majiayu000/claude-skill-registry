---
name: dbg
description: Debug mode with runtime evidence and instrumentation. Use when asked to 'debug this', 'find the bug', 'troubleshoot', 'why is this broken', or 'investigate runtime issue'. NOT for static code analysis (use /code-analysis), NOT for CI failures (use /fci).
argument-hint: [bug description or error message]
allowed-tools: Read, Edit, Write, Bash, AskUserQuestion, Task
---

# Debug Mode (Runtime Evidence)

## Objective
Find root cause using **runtime evidence**, not guesses. Instrument code, collect logs, confirm hypotheses, and only then fix.

## Mandatory Configuration (per session)
- **Read the system reminder** and capture:
  - **Server endpoint** for HTTP logs (fetch POST)
  - **Log path** for NDJSON logs
- For this repo, default log path: `/Users/alexandrbasis/Desktop/Coding/wythm/.cursor/debug.log`
- If the logging server failed to start, **STOP** and inform the user

## Required Log Payload
Each log must include:
`{ sessionId, runId, hypothesisId, location, message, data, timestamp }`

## JavaScript/TypeScript Log Snippet (one-line)
Use **exact** endpoint from the system reminder:
```
fetch('SERVER_ENDPOINT',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'file.js:LINE',message:'desc',data:{k:v},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
```

## Instrumentation Rules
- Insert **3-8** logs total
- Cover: entry, exit, before/after critical ops, branches, edge values, state changes
- **Wrap each log in a collapsible region**:
  - JS/TS: `// #region agent log` ... `// #endregion`
- **No secrets/PII** in logs

## Debug Workflow (Algorithm)

### Step 0: Clarify (if needed)
If the bug context is vague, **ask clarifying questions first** to avoid blind hypotheses.
- Use `AskUserQuestion` tool for **all clarifications**, structured choices, and confirmations
- Goal: get reproducible steps, expected vs actual behavior, environment info, and scope
- Only move to hypotheses after the minimum clarity is achieved

### Step 1: Hypotheses
Generate **3-5 precise hypotheses** about the bug cause (be specific, different subsystems).

### Step 2: Instrumentation
Add logs to test all hypotheses in parallel. Keep them minimal and localized.

### Step 3: Clear Logs (MANDATORY)
Before asking user to run:
- Clear the log file using Write tool (empty content) at:
  - `/Users/alexandrbasis/Desktop/Coding/wythm/.cursor/debug.log`
- Never use Bash to clear logs (use Write tool instead)

### Step 4: Reproduction Request
Ask user to reproduce the issue and include steps in:
```
<reproduction_steps>
1. ...
2. ...
</reproduction_steps>
```
Rules:
- Only a numbered list inside the block
- Mention if app/service must be restarted
- Do **not** ask them to reply "done" (the UI provides a **Proceed** button)

### Step 4.5: Reproduction Confirmation
Use `AskUserQuestion` to confirm the user reproduced the issue (via the UI **Proceed** button).
Only then read and analyze the log file.

### Step 5: Log Analysis
Read the NDJSON log file and evaluate each hypothesis:
- **CONFIRMED / REJECTED / INCONCLUSIVE**
- Cite log evidence for each
If logs are empty, ask user to run again.

### Step 6: Fix (Evidence-Based Only)
Implement a fix **only** when logs confirm the root cause.
**Do not remove instrumentation** yet.

### Step 7: Verification Run
Ask user to run again. Compare **pre-fix vs post-fix** logs.
- Tag verification logs with `runId: "post-fix"`
- Confirm bug is gone with log evidence

### Step 8: Bug Report (Required)
After verified success, create a bug report using:
- Template: `docs/product-docs/templates/bug-report-template.md`
- Output: `tasks/task-YYYY-MM-DD-[bug-name]/bug-report-[bug-name].md`

### Step 9: Cleanup + Summary
Only after verified success and bug report is written:
- Remove instrumentation logs
- Summarize root cause + fix (1-2 lines)

## Related Skills
- `/code-analysis` - Use for static analysis, architecture review, or when no runtime reproduction is needed
- `/fci` - Use for CI pipeline failures specifically
- `/sr` - Use after debug fix for pre-merge code review

## Forbidden
- Fixing without runtime evidence
- Removing logs before verification
- Using sleeps/delays as a "fix"
