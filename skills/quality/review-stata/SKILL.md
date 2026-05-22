---
name: review-stata
description: Run the Stata code review protocol on .do files in code/stata/. Checks reproducibility, variable management, regression specification, table and figure output conventions. Produces a report without editing files.
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review Stata Scripts

Run the comprehensive Stata code review protocol.

## Steps

1. **Identify scripts to review:**
   - If `$ARGUMENTS` is a specific `.do` filename or path: review that file only
   - If `$ARGUMENTS` is `all`: review all `.do` scripts in `code/stata/`

2. **For each script, launch the `stata-reviewer` agent** with instructions to:
   - Follow the full protocol in `.claude/agents/stata-reviewer.md`
   - Read `.claude/rules/stata-code-conventions.md` for current standards
   - Save report to `quality_reports/[script_name]_stata_review.md`

3. **After all reviews complete**, present a summary:
   - Total issues found per script
   - Breakdown by severity (Critical / High / Medium / Low)
   - Top 3 most critical issues across all scripts

4. **IMPORTANT: Do NOT edit any Stata source files.**
   Only produce reports. Fixes are applied after user review.
