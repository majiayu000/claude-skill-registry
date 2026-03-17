---
name: prime-sync
description: Sync Claude config between prime repo and target projects (push from prime or pull from target)
argument-hint: "[<target-project-path>] (push mode only, optional in pull mode)"
disable-model-invocation: true
---

Ultrathink.

## Role

You are a sync orchestrator. Analyze and sync Claude configurations between prime and target projects.

## Mode Detection

Detect operating mode before anything else:

1. `VERSION` file exists in CWD → **push mode** (CWD is the prime repo)
2. `.claude/.prime-version` exists in CWD → **pull mode** (CWD is a target project)
3. Neither detected → ask user which mode and for the required path

## Push Mode — Resolve Target

Source = CWD (prime repo). Target = resolved project path.

**State file:** `.claude/prime-projects.json`
```json
{
  "projects": [
    { "path": "/absolute/path", "lastSynced": "2025-12-30T10:30:00Z", "version": "1.4.2" }
  ]
}
```

**Resolution flow:**
1. **Argument provided** → Use path directly, save to state after sync
2. **No argument, state file has projects** → Ask user (multiSelect, include "All projects" option)
3. **No argument, no state file** → Ask user for path

**State file management:**
- Create `.claude/` if needed
- Update `lastSynced` and `version` after successful sync
- No duplicate paths

## Pull Mode — Clone Prime

Source = cloned prime repo. Target = CWD.

**Flow:**
1. Read current version from `.claude/.prime-version` in CWD
2. Generate timestamp: `date +%Y%m%d%H%M%S`
3. Clone prime repo: `git clone https://github.com/avibebuilder/claude-prime.git /tmp/claude-prime-sync-<timestamp>/`
4. Set source = `/tmp/claude-prime-sync-<timestamp>/`, target = CWD
5. Continue to shared process below
6. Clean up `/tmp/claude-prime-sync-<timestamp>/` after sync completes (success or failure)

No state file in pull mode — the target project is self-contained.

## Process

Check conversation context and skip completed steps.

### 1. Validate Target
- Check path exists and is a valid project
- Read versions from target (`.claude/.prime-version`) and prime (`VERSION`)

If invalid → abort with error.

### 2. Parallel Analysis

**Change Detection**:
- Detect git changes in prime's `.claude/` based on version state
- If `NO_VERSION` or `SAME_VERSION` → uncommitted changes only
- If `DIFFERENT_VERSION` → diff from tag to HEAD + uncommitted (warn if tag missing)
- Categorize: commands, agents, hooks, settings, skills, starter-skills

**Stack Detection** (only if skills or starter-skills changed):
- For each changed skill/starter, check if target has matching stack indicators
- Only scan indicators relevant to that skill/starter

**File Comparison**:
- Compare each changed file with target
- Detect: NEW, UPDATE, IDENTICAL, CONFLICT

### 3. Build Sync Plan
Aggregate results and present:
```
CHANGED (will sync): ...
IDENTICAL (skip): ...
CONFLICTS (will ask): ...
IRRELEVANT (skip, wrong stack): ...
```

**GATE**: User approves sync plan.

### 4. Handle Conflicts
For each conflict, show diff and ask user:
- **Overwrite** — Replace with prime version
- **Skip** — Keep target version
- **Merge** — Show full diff for selection

### 5. Execute Sync
1. Create `.claude/` in target if needed
2. Copy approved files (skills as entire folders)
3. Sync approved starter-skills to `.claude/starter-skills/` in target
4. Update `.prime-version` with prime's VERSION

### 6. Report
```
Sync complete! (prime vX.X.X)
Updated: ...
Skipped: ...
Version: X.X.X → written to .prime-version
```

Push mode only: update state file (`lastSynced` timestamp + `version`).
Pull mode only: clean up `/tmp/claude-prime-sync-*` clone directory.

## Constraints

- NEVER sync `prime-sync` skill — it belongs only in prime repo
- NEVER touch: `project/`, `.mcp.json`, `settings.local.json` in target
- NEVER modify target project's source code or run commands in target
- NEVER sync without user approval at the gate
- NEVER lose project history — append to state file, no duplicates (push mode)
- ALWAYS clean up `/tmp` clone after sync, even on failure (pull mode)
- NEVER use state file in pull mode — target is self-contained

## Target Path

<target-path>$ARGUMENTS</target-path>
