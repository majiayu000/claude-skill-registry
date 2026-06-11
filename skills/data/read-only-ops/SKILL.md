---
name: read-only-ops
description: "Read-only exploration, inspection, and reporting without modifications. Explore and report on code/config/state without writing or modifying anything."
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
routing:
  triggers:
    - "inspect without changing"
    - "report only no edits"
    - "audit current state"
    - "explore code"
    - "read-only"
    - "browse code"
    - "inspect only"
  category: process
  pairs_with:
    - codebase-overview
---

# Read-Only Operations Skill

## Overview

This skill operates as a safe exploration and reporting mechanism without ever modifying files or system state. Use it when you need to gather evidence, verify facts, or show current state to the user.

The core principle: **Observation Only**. Gather evidence. Report facts. Keep all state unchanged.

---

## Instructions

### Phase 1: SCOPE

**Goal**: Understand exactly what the user wants to know before exploring.

**Step 1: Parse the request**

Determine:
- What specific information is the user asking for?
- What is the target scope (specific file, directory, service, system-wide)?
- Are there implicit constraints (time range, file type, component)?

**Step 2: Confirm scope if ambiguous**

If the request could match dozens of results or span the entire filesystem, clarify before proceeding. If the scope is clear, proceed directly. This prevents wasting tokens on over-broad searches.

**Gate**: Scope is understood. Target locations are identified. Proceed only when gate passes.

---

### Phase 2: GATHER

**Goal**: Collect evidence using read-only tools. Tools must preserve state.

**Step 1: Execute read-only operations**

**Allowed commands** (safe for read-only use):
```
ls, find, wc, du, df, file, stat
ps, top -bn1, uptime, free, pgrep
git status, git log, git diff, git show, git branch
sqlite3 ... "SELECT ..."
curl -s (GET only)
date, timedatectl, env
```

**Out-of-scope commands** (are outside the read-only boundary):
```
mkdir, rm, mv, cp, touch, chmod, chown
git add, git commit, git push, git checkout, git reset
echo >, cat >, tee (file writes)
INSERT, UPDATE, DELETE, DROP, ALTER SQL
npm install, pip install, apt install
pkill, kill, systemctl restart/stop
```

Rationale: Even "harmless" state changes violate the read-only boundary. Use the read-only equivalent instead (e.g., `ls -la` instead of `mkdir -p`, `git status` instead of `git add`, `SELECT` instead of `INSERT`).

**Step 2: Record raw output**

Show complete command output. Show complete output, truncating only unless output exceeds reasonable display length, in which case show representative samples with counts. The user must be able to verify your claims from the evidence shown.

**Gate**: All requested data has been gathered with read-only commands. No state was modified. Proceed only when gate passes.

---

### Phase 3: REPORT

**Goal**: Present findings in a structured, verifiable format.

**Step 1: Summarize key findings at the top**

Lead with what the user asked about. Answer the question first, then provide supporting details. This prevents burying the answer in verbose output.

**Step 2: Show evidence**

Include command output, file contents, or search results that support the summary. The user must be able to verify claims from the evidence shown. Show the raw data — show the raw data.

**Step 3: List files examined**

Document which files were read for transparency:

```markdown
### Files Examined
- `/path/to/file1` - why it was read
- `/path/to/file2` - why it was read
```

**Gate**: Report answers the user's question with verifiable evidence. All claims are supported by shown output.

---

## Error Handling

### Error: "Attempted to use Write or Edit tool"
**Cause**: Skill boundary violation — tried to modify a file.
**Solution**: This skill only permits Read, Grep, Glob, and read-only Bash. Report findings verbally; write them to files only with explicit user permission. Crossing the read-only boundary defeats the purpose of the skill.

### Error: "Bash command would modify state"
**Cause**: Attempted destructive or state-changing command.
**Solution**: Use the read-only equivalent. For example:
- `ls -la` instead of `mkdir -p`
- `git status` instead of `git add`
- `SELECT` instead of `INSERT`
- `stat` or `[ -d /path ] && echo exists` instead of `mkdir -p /tmp/test`

### Error: "Scope too broad, results overwhelming"
**Cause**: Search returned hundreds of matches without filtering.
**Solution**: Return to Phase 1. Narrow scope by file type, directory, or pattern before re-executing. For example, instead of searching the entire filesystem for "config", search `~/.config/` or `./etc/` with a specific file extension.

### Preferred Patterns

**Investigating Everything**: User asks about API server status; you audit all services, configs, logs, and dependencies. Why wrong: Wastes tokens, buries the answer. The scope extends beyond the specific question. Do instead: Answer the specific question. Offer to investigate further if needed.

**Summarizing Away Evidence**: "The repository has 3 modified files and is clean" instead of showing `git status` output. Why wrong: User cannot verify the claim. Missing details (which files? staged or unstaged?) prevent verification. Do instead: Show complete command output. Let the user draw conclusions.

**Exploring Before Scoping**: User says "find config files"; you immediately search entire filesystem. Why wrong: May return hundreds of irrelevant results. Wastes time without direction. Do instead: Confirm scope (which config? where? what format?) then search targeted locations.

---

## References

### Skill Design Philosophy

This skill enforces the **Observation Only** architectural pattern to enable safe, passive exploration without side effects. The constraint is absolute: tools must preserve state, even to "verify" something. Verification that requires modification (e.g., "is this directory writable?") should use read-only checks (`stat`, `ls -la`, test operators).

### CLAUDE.md Compliance

This skill follows the CLAUDE.md principle of verification over assumption and artifacts over memory. All claims are backed by shown evidence. No paraphrasing. No hidden state changes.
