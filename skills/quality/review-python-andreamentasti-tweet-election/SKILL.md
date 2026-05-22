---
name: review-python
description: Run the Python code review protocol on scripts in code/py/. Checks code quality, reproducibility, pandas idioms, figure standards, and output conventions. Produces a report without editing files.
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review Python Scripts

Run the comprehensive Python code review protocol.

## Steps

1. **Identify scripts to review:**
   - If `$ARGUMENTS` is a specific `.py` filename or path: review that file only
   - If `$ARGUMENTS` is `all`: review all `.py` scripts in `code/py/`
     (skip `config.py` unless explicitly requested — it's a config file, not an analysis script)

2. **For each script, launch the `python-reviewer` agent** with instructions to:
   - Follow the full protocol in `.claude/agents/python-reviewer.md`
   - Read `.claude/rules/python-code-conventions.md` for current standards
   - Read `code/py/config.py` to understand the path configuration
   - Save report to `quality_reports/[script_name]_python_review.md`

3. **After all reviews complete**, present a summary:
   - Total issues found per script
   - Breakdown by severity (Critical / High / Medium / Low)
   - Top 3 most critical issues across all scripts

4. **IMPORTANT: Do NOT edit any Python source files.**
   Only produce reports. Fixes are applied after user review.
