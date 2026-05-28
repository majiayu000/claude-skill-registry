---
name: land
description: "End session. Reconciles exploration folders, appends context to CAPCOM, syncs Beads, displays session stats."
---

# /land - End Session

Capture session context in CAPCOM and reconcile any folder states that were missed during the session.

## Procedure

### Step 0: Reconcile Exploration Folders

Check for folder/state mismatches and fix them:

| If folder in... | But has... | Move to... |
|-----------------|------------|------------|
| `exploration/ideas/` | `plan.md` | `exploration/planned/` |
| `exploration/planned/` | Beads feature exists | `mission/staged/` |
| `mission/staged/` | Beads feature closed | `mission/complete/` |

For each mismatch: show user, confirm, then `mv` the folder.

### Step 1: Gather State

```bash
git branch --show-current
git status --short
git log -1 --oneline
bd stats
bd list -t feature --status in_progress
```

From your session memory, note:
- Tasks completed this session
- Bugs fixed this session
- Active feature and its progress (done/total tasks)

### Step 2: Append to CAPCOM

Get next session number:
```bash
grep -c "^## \[.*\] Session [0-9]" .space-agents/comms/capcom.md 2>/dev/null || echo 0
```
Add 1 to get the next session number.

Append full session context to `.space-agents/comms/capcom.md`:

```markdown
## [YYYY-MM-DD HH:MM] Session {N}

**Branch:** {branch} | **Git:** {clean/uncommitted}

### What Happened
[Narrative of what was worked on. Be specific - file names, function names, what changed and why.]

### Decisions Made
[Architectural decisions, trade-offs chosen, "we decided X because Y". Skip if none.]

### Gotchas
[Things that surprised you, bugs encountered, "watch out for X". Skip if none.]

### In Progress
[If stopped mid-task: what state, next step, files involved. Skip if clean stop.]

### Next Action
[One clear thing to do next session.]

---
```

**Guidelines:**
- Be specific ("added JWT refresh in auth/tokens.ts:45" not "updated auth")
- Include file paths where relevant
- Capture reasoning, not just actions
- Skip empty sections
- CAPCOM is append-only

### Step 3: Land

**Pre-flight:**
```bash
bd doctor --quiet    # Warn on failures, don't block
git status           # Review pending changes
```

**Stage and commit:**
```bash
git add <specific files>   # Stage code changes (not -A)
bd sync                    # Sync beads
git commit -m "feat: <summary from session>"   # Meaningful message
git push
```

Commit message should summarize session work (e.g., "feat: update agent terminology, complete feature 1.2").

### Step 4: Display Summary

Query features and show progress:

```bash
bd list -t feature
bd list --tree
```

Output format:
```
SESSION COMPLETE
────────────────
Tasks completed: {count from session}
Bugs fixed:      {count from session}

FEATURES
{for each feature from bd list -t feature}
{status_icon} {feature_title}  [{closed_tasks}/{total_tasks}]
{end for}

Context saved to CAPCOM. Run /launch to continue.
Safe travels, Commander.
```

**Status icons:** ✓ closed, ◐ in_progress, ○ open, ● blocked
