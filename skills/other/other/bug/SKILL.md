---
name: bug
description: Use when the user provides error logs, stack traces, crash reports, or describes broken functionality that needs investigation and an architectural fix plan.
invocation: agent
---

# Bug Investigation & Fix Planning

Investigate bugs from any input — error logs, stack traces, user reports. Creates an architectural fix plan with exact code specifications.

**Use the right skill:**
- **Bug fixes** → `bug` (this skill)
- **Quick debugging** → `debug`
- **New features** → plan via `/arc:core:plan`
- **Code quality** → `quality`

**Note**: Only view-only git commands allowed (no state modifications).

## Arguments

Takes any input:
- Error logs: `"TypeError: 'NoneType' at auth.py:45"`
- Stack traces: `"$(cat stacktrace.txt)"`
- Log files: `./logs/error.log`
- User reports: `"Login fails when user has no profile"`
- Diagnostic instructions: `"Check docker logs for api-service"`

## Instructions

### Step 1: Process Input

Parse input:
- If file path → use Read tool to load contents
- If inline text → extract error signals
- If diagnostic instructions → execute via Bash:
  - Docker logs: `docker logs <container> --tail 500`
  - Process logs: `journalctl -u <service>`

### Step 2: Launch Agent

Launch background agent with gathered context:

**REQUIRED Task tool parameters:**
```
subagent_type: "arc:bug-plan-creator"
run_in_background: true
prompt: "Investigate bug and create fix plan:\n\n<gathered context>"
```

Output a status message like "Investigating bug..." and **end your turn**. The system wakes you when the agent finishes.

### Step 3: Report Result

```
## Bug Investigation Complete

**Plan**: openspec/plans/YY-MM-DD-bug-<name>-<hash5>.md
**Severity**: [Critical/High/Medium/Low]
**Root Cause Confidence**: [High/Medium/Low]

Root Cause: [file:line] - [brief description]

Next Steps:
1. Review the fix plan
2. Execute: `/arc:core:execute --source plan --plan-path <plan-path>`
```

## Error Handling

| Scenario | Action |
|----------|--------|
| Log file missing | Report error, continue with other data |
| Diagnostic fails | Report error, continue |
| Low confidence | Highlight, recommend review |
| No bug found | Report external/config causes |
