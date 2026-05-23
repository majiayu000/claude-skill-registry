---
name: jj-context
description: Show current commit status and changes from trunk in jj
---

# /jj-context - Show Current Context

Display the current jj working copy status and all changes from trunk.

## Instructions

1. **Show current status**: Run `jj status` to see the current working copy status, including:
   - Modified files in the working copy
   - The current commit's parent(s)
   - Any conflicts

2. **Show commits from trunk**: Run `jj log -r 'trunk()..@'` to see all commits between trunk and the current working copy. This shows the commit history of your current work.

3. **Get change overview**: Run these commands to understand the scope of changes from trunk:
   - `jj diff -r 'trunk()..@' --summary` - List of files with change type (modified/added/deleted)
   - `jj diff -r 'trunk()..@' --stat` - Histogram showing lines changed per file

4. **Analyze the changes**:
   - **For small changes** (≤10 files, ≤300 lines total): Run `jj diff -r 'trunk()..@'` directly to see the full diff
   - **For large changes** (>10 files or >300 lines): Use the **Task tool** with `subagent_type=Explore` to analyze:
     ```
     prompt: "Run `jj diff -r 'trunk()..@'` and provide a structured summary: 1) Group changes by directory/subsystem 2) Describe the key modifications in each area 3) Note any significant additions or deletions. Keep each section brief."
     ```

5. **Present the context**: Display to the user:
   - Current status
   - Commit log from trunk
   - Files changed summary (from --summary)
   - For small diffs: the actual diff; for large diffs: the Task agent's summary

## Notes

- `trunk()` in jj refers to the main branch (typically `main` or `master`)
- The `..` range includes all commits between the two revisions
- This is useful for understanding the full scope of work before creating a PR or reviewing changes
