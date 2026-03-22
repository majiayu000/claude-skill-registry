---
name: write-report
description: >
  Generates a human-readable markdown review report from an xreview session.
  Invoked automatically by the xreview skill at Step 5 after a review is complete,
  or manually via /write-report <session-id>. Combines structured session data
  with conversation context (verification results, user decisions, fix details)
  to produce a comprehensive, readable report.
allowed-tools: Bash(xreview *), Read, Write
argument-hint: <session-id>
---

# write-report — Generate Review Report

## Step 1: Get session data

Run: `xreview report --session <session-id>`

Parse the XML output to extract:
- Session ID and round count
- Finding list with final statuses (open / fixed / dismissed)
- Summary counts (total, open, fixed, dismissed)
- Report file path (the JSON data xreview saved)

If the command fails, show the error to the user and stop.

## Step 2: Generate markdown report

Combine the structured session data with what you recall from the conversation:

- **Verification results** — which findings you confirmed or suspected, and why
- **User decisions** — what the user chose to fix, skip, or adjust
- **Fix details** — what code changes you made for each finding
- **Dismissal reasons** — why certain findings were not fixed

Write the report using this layout:

```markdown
# Code Review Report

**Date:** YYYY-MM-DD
**Session:** <session-id>
**Reviewed:** <list of files or "uncommitted changes">
**Rounds:** <number of review rounds>

## Context

<The --context provided for this review.
Include what was reviewed, why, and what the reviewer should focus on.>

## Summary

| Status | Count |
|--------|-------|
| Total findings | N |
| Fixed | N |
| Dismissed | N |
| Open | N |

## Findings

### F-XXX: <title> — <severity>/<category> ✅ Fixed

**Location:** `file.go:42`
**Issue:** <description of the problem>
**Fix applied:** <what was changed and why this approach was chosen>

### F-XXX: <title> — <severity>/<category> ⏭️ Dismissed

**Location:** `file.go:10`
**Issue:** <description>
**Reason:** <why — user decision, false positive confirmed by Codex discussion, etc.>

### F-XXX: <title> — <severity>/<category> ⚠️ Open

**Location:** `file.go:99`
**Issue:** <description>
**Note:** <why this remains open — deferred to next PR, needs more context, etc.>

## Open Items

<If any findings remain open, summarize what's left and recommended next steps.
If everything is resolved, write "All findings have been addressed.">
```

**Layout rules:**
- Group findings by status: Fixed first, then Dismissed, then Open
- For Fixed findings: describe what was actually changed, not just the original suggestion
- For Dismissed findings: always include the reason
- Use emoji status markers consistently: ✅ Fixed, ⏭️ Dismissed, ⚠️ Open
- Keep descriptions concise — the report is a record, not a tutorial

## Step 3: Save and present

1. **Save the full report** to `.xreview/reports/<session-id>.md`
   using the Write tool.

2. **Print a summary in the conversation:**

```
Review complete. Report saved to .xreview/reports/<session-id>.md

Summary: N findings — X fixed, Y dismissed, Z open.
```

3. **Clean up session** — run `xreview clean --session <session-id>`.
   The session data is no longer needed after the report is saved.
