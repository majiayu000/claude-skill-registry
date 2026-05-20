---
name: report-bug
categories: [github]
description: Investigate a bug from provided error context, write a structured markdown report to the given path, and output a deduplication fingerprint. Lightweight — no parallel subagents.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '[SKILL: report-bug] Investigating bug...'"
          once: true
---

# Report Bug Skill

Perform a targeted bug investigation from a provided error context and produce a structured report. This skill is intentionally lightweight — it performs a directed codebase search rather than spawning parallel subagents, so it stays fast enough for non-blocking pipeline use.

## Input Format

The prompt will contain:

```
Error context:
<error message, traceback, or free-form description>

Report output path: /absolute/path/to/report.md
```

## Critical Constraints

**NEVER:**
- Modify any source code files
- Create files other than the specified report output path
- Spawn subagents or Agent tool calls

**ALWAYS:**
- Write the completed report to the exact path specified in "Report output path"
- Include the fingerprint block (see below) in your **response text** (stdout), not in the report file
- Keep the fingerprint under 80 characters

## Investigation Workflow

### Step 1: Parse Inputs

Extract from the prompt:
- `error_context`: everything under "Error context:"
- `report_path`: the absolute path after "Report output path:"

### Step 2: Identify the Error

From the error context:
- Extract error type (e.g. `KeyError`, `AssertionError`, `TypeError`)
- Extract the failing callsite (file + line if present in a traceback)
- Identify the primary affected module from the path or import chain

### Step 3: Targeted Codebase Search

Use Grep and Read to locate the relevant callsite and understand the surrounding logic:
1. Search for the error message string or function name in the codebase
2. Read the failing function body
3. Check for similar patterns nearby that succeed (to understand the invariant that broke)
4. Look for the most recent change to the file (git context if available)

Keep searches focused — 3–5 targeted queries is sufficient.

### Step 4: Produce the Fingerprint

Synthesise a canonical bug description of ≤ 80 characters that uniquely identifies
the bug class (not the specific stack frame). This is used for GitHub deduplication.

Format: `<ErrorType> in <module>: <one-line cause>`

Examples:
- `KeyError in recipe/validator.py: missing ingredient ref in step capture`
- `AssertionError in execution/headless.py: runner=None before session start`

### Step 5: Write the Report File

Use the Write tool to write the structured report to the exact path from the prompt.

Report template:
```markdown
# Bug Report

**Date:** {YYYY-MM-DD}
**Error type:** {error type}
**Affected module:** {file path}

## Error Context

```
{verbatim error_context}
```

## Callsite

**File:** {file}:{line}
**Function:** {function name}

## Root Cause Hypothesis

{1–3 sentences explaining the likely root cause}

## Relevant Code

```python
{the failing function or the surrounding ~10 lines}
```

## Recommended Action

{Concise next step — e.g. "Check X before Y", "Add guard for Z condition"}
```

### Step 6: Output the Fingerprint Block

After writing the report file, output the following in your response text so the
calling tool can extract it for GitHub deduplication:

```
---bug-fingerprint---
{the fingerprint from Step 4}
---/bug-fingerprint---
```

Then confirm: `Report written to {report_path}`
