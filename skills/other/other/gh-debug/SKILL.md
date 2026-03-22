---
name: gh-debug
description: Debug GitHub Actions build failures by fetching and analyzing workflow logs. Use when CI/CD pipelines fail and you need to identify the root cause.
argument-hint: [run-id or workflow-url]
context: fork
---

Pull GitHub Actions logs for a workflow run, parse them to identify errors, and provide a clear diagnostic report.

Arguments: $ARGUMENTS

**Primary Method (Recommended)**: Use the Python script for efficient log analysis:
```bash
uv run ci/tools/gh_debug.py $ARGUMENTS
```

This script:
- Streams logs instead of downloading full files (avoids 55MB+ downloads)
- Filters for errors in real-time
- Stops after finding 10 errors (configurable with --max-errors)
- Shows context around each error (5 lines before/after, configurable with --context)

**Fallback Method**: If the Python script fails, use manual analysis:

## Smart Log Fetching Strategy

1. **Identify failed jobs/steps** using `gh run view <run-id> --log-failed`
2. **For each failed step**, use targeted log extraction with grep filters
3. **Parse logs** for: compilation errors, test failures, runtime issues
4. **Extract error context**: ~10 lines before and after each error

## Input Handling

Handle:
- Run IDs (e.g., "18391541037")
- Workflow URLs
- Most recent failed run if no argument provided (use `gh run list --status failure --limit 1`)

## Output Format

Provide:
- Workflow name and run number
- Job(s) that failed with step names
- Specific error messages with surrounding context (max ~50 lines per error)
- File paths and line numbers where applicable
- Suggested next steps or potential fixes
