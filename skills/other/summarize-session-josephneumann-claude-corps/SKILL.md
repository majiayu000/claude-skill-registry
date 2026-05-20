---
name: summarize-session
description: "Use for a read-only progress snapshot without committing, pushing, or closing anything"
allowed-tools: Read, Bash, Glob, Grep
---

# Summarize Session: $ARGUMENTS

Generate a comprehensive session summary for task `$ARGUMENTS`. This is a standalone command that ONLY generates the summary - it does NOT commit, push, close the task, or make any changes.

## 1. Gather Context

```bash
bd show $ARGUMENTS
git status
git log --oneline -10
git diff --stat HEAD~5 2>/dev/null || git diff --stat
pwd
```

## 2. Identify Changed Files

```bash
# Files changed in recent commits
git diff --name-only HEAD~5 2>/dev/null || git diff --name-only

# New files created
git diff --name-only --diff-filter=A HEAD~5 2>/dev/null

# Files modified
git diff --name-only --diff-filter=M HEAD~5 2>/dev/null
```

Read key files to understand what was implemented.

## 3. Check Test Status

```bash
# Get test counts
uv run pytest --collect-only -q 2>/dev/null | tail -5
# Or
pnpm test 2>/dev/null | tail -10
```

## 4. Check Unblocked Tasks

```bash
bd dep tree $ARGUMENTS 2>/dev/null || echo "No dependency info"
```

## 5. Re-Read Original Task Spec

**CRITICAL**: Before writing the session summary, re-read the original task specification to accurately identify divergences:

```bash
bd show $ARGUMENTS
```

Save this output mentally - you'll compare it against your implementation when writing the SPEC DIVERGENCES section. Don't rely on memory; divergences are easy to miss without explicit comparison.

## 6. Generate Session Summary

**IMPORTANT**: Output a detailed session summary for orchestrating agents. This summary will be consumed by a coordinating agent to track progress across multiple parallel work sessions. Be verbose and thorough.

Use this exact format:

```
===============================================
SESSION SUMMARY: <Task Title>
===============================================

TASK OVERVIEW
-------------
ID: $ARGUMENTS
Title: <title from bd show>
Status: <current status>
Priority: <P1/P2/P3 from bd show>
Type: <feature/task/bug from bd show>

INTENT & SCOPE
--------------
What this task set out to accomplish:
<2-3 sentences explaining the goal of this task in plain language. What problem does it solve? Why was it needed?>

IMPLEMENTATION SUMMARY
----------------------
<Narrative description of what was built. Write 3-5 sentences explaining the approach taken, key design decisions, and how the pieces fit together. An orchestrating agent should be able to understand the work without reading the code.>

FILES CREATED
-------------
<For each new file, include path and brief description>

1. <path/to/file.py>
   Purpose: <what this file does>
   Key components: <main classes/functions>
   Lines: <approximate line count>

2. <path/to/file.py>
   ...

FILES MODIFIED
--------------
<For each modified file, explain what changed and why>

1. <path/to/file.py>
   Changes: <what was added/changed>
   Reason: <why this change was needed>

2. <path/to/file.py>
   ...

TESTS
-----
New tests added: <count>
Total tests now passing: <count>
Test file(s): <path(s)>

Key test coverage:
- <what scenarios are tested>
- <what edge cases are covered>

DOCUMENTATION UPDATED
---------------------
<List each doc file updated with a brief note on what changed, or "None required">

GIT ACTIVITY
------------
Branch: <branch-name>
Commits: <count in this session>
PR: <URL or "Not created">
Merged to: <target branch or "Not merged">
Model: <opus|sonnet|inherited>

BEADS STATUS
------------
Task closed: <Yes/No>
Reason: <close reason or "Still in progress">
Synced to remote: <Yes/No>

SPEC DIVERGENCES
----------------
Compare your implementation against the original task description from `bd show`. Document ANY differences between what was specified and what was actually built. Be explicit and thorough - the orchestrator relies on this to keep the task board accurate.

Format each divergence as:

**Divergence N: <brief title>**
- Specified: <what the task description said to do>
- Implemented: <what was actually built>
- Reason: <why the change was necessary - technical constraint, better approach discovered, dependency issue, etc.>
- Impact: <what downstream tasks or specs need updating>

If implementation matched spec exactly, state: "None - implementation matches specification."

Examples of divergences to document:
- Different file structure than specified
- Added/removed features from original scope
- Changed API contracts or schemas
- Used different libraries or approaches
- Deferred functionality to follow-up tasks
- Discovered requirements that weren't in the spec

FOLLOW-UP ISSUES CREATED
------------------------
<List any new beads issues created during this session, or "None">

DEPENDENCIES UNBLOCKED
----------------------
The following tasks were blocked by this task and can now proceed:
<List each task ID and title, or "None">

ARCHITECTURAL NOTES
-------------------
<Any important technical decisions, patterns established, or constraints discovered that future work should be aware of. This helps maintain consistency across parallel agent sessions.>

HANDOFF CONTEXT
---------------
<What should the next agent or session know? Include:
- Any gotchas or things that didn't work as expected
- Assumptions made that might need revisiting
- Suggested next steps if continuing related work
- Dependencies on external systems or APIs
- Performance considerations if any>

===============================================
END SESSION SUMMARY
===============================================
```

This format ensures orchestrating agents have full context to coordinate parallel work and make informed decisions about task assignment.

## 7. Persist Summary to Disk

Write the summary to a file so orchestrating agents can read it directly from disk.

```bash
# Get project root (handles worktrees correctly)
PROJECT_ROOT=$(git rev-parse --show-toplevel)

# Create directory if needed
mkdir -p "$PROJECT_ROOT/docs/session_summaries"

# Add to .gitignore if not present
if ! grep -q "^docs/session_summaries/$" "$PROJECT_ROOT/.gitignore" 2>/dev/null; then
  echo "docs/session_summaries/" >> "$PROJECT_ROOT/.gitignore"
fi

# Generate filename with timestamp
TIMESTAMP=$(date +%y%m%d-%H%M%S)
SUMMARY_FILE="$PROJECT_ROOT/docs/session_summaries/$ARGUMENTS_${TIMESTAMP}.txt"
```

Write the summary content using a heredoc:

```bash
cat > "$SUMMARY_FILE" <<'SUMMARY_EOF'
<paste the full session summary content here>
SUMMARY_EOF

echo "Summary written to: $SUMMARY_FILE"
```

**Important:** The summary file allows orchestrators to asynchronously review completed work without needing the worker session to remain active.

## 8. Copy to Clipboard (Optional)

Use AskUserQuestion to offer copying the summary to clipboard:

**Question:** "Copy session summary to clipboard?"
- **Options:** "Yes, copy to clipboard" / "No, skip"
- **Header:** "Clipboard"

If the user selects "Yes, copy to clipboard":

```bash
cat "$SUMMARY_FILE" | pbcopy
echo "Summary copied to clipboard"
```

This avoids clipboard conflicts when multiple worker sessions complete simultaneously.
