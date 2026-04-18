---
name: prime-sync
description: "Syncs Claude config between prime repo and target projects. Trigger on 'sync', 'prime-sync', 'push config', 'pull config', 'update prime', 'sync claude config'. Push mode deploys to targets; pull mode imports changes back."
argument-hint: "[<target-project-path>] (push mode only, optional in pull mode)"
disable-model-invocation: true
---

Ultrathink.

## Mode Detection

Detect operating mode before anything else:

1. `VERSION` file exists in CWD → **push mode** (CWD is the prime repo)
2. `.claude/.prime-version` exists in CWD → **pull mode** (CWD is a target project)
3. Neither detected → ask user which mode and for the required path

## Push Mode — Resolve Target

Source = CWD (prime repo). Target = resolved project path.

**State file:** `.claude/prime-projects.json`

Tracks known target paths, last sync time, and version. Shape:
```json
{ "projects": [{ "path": "/absolute/path", "lastSynced": "2025-12-30T10:30:00Z", "version": "1.4.2" }] }
```
Create as `{ "projects": [] }` if missing.

**Resolution flow:**
1. **Argument provided** → Use that path, then record it after a successful sync
2. **No argument, known projects exist** → Ask the user which project(s) to sync, including an **All projects** option
3. **No argument, no known projects** → Ask the user for a path

**State file management:**
- Create `.claude/` only if you need to persist the state file
- Update the synced project's time/version only after a successful sync
- Keep one entry per absolute path

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

### 1. Validate Target
- Check that the target path exists, is a directory, and is not the same location as the source repo
- Treat a valid target as a project root where writing `.claude/` is appropriate
- Read versions from target (`.claude/.prime-version`) and prime (`VERSION`)

If the path fails those checks, abort and explain why.

### 2. Parallel Analysis

**Change Detection**:
- Detect relevant changes in prime's `.claude/` based on the target's recorded version state
- If the target has no recorded version, or already matches the current prime version, sync only uncommitted prime changes
- If the target is on an older prime version, diff from that version tag to `HEAD` and include uncommitted changes; warn if the tag is missing
- Categorize changes into commands, agents, hooks, settings, skills, and starter-skills

**Stack Detection** (only if skills or starter-skills changed): check target for stack indicators relevant to each changed skill/starter.

**File Comparison**: compare each changed file with target. Detect: NEW, UPDATE, IDENTICAL, CONFLICT.

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
For each conflict, show the relevant diff and ask the user how to proceed:
- **Overwrite** — Replace the target copy with the prime version
- **Skip** — Leave the target copy unchanged
- **Merge** — Surface the full diff and let the user choose which parts to keep before writing anything

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

## Gotchas

- **`prime-sync` stays in prime** — do not copy this skill into target projects.
- **Push and pull keep different state** — state file is push-only; pull mode treats the target as self-contained.
- **Version history can be incomplete** — if the expected tag is missing, warn and continue with that uncertainty explicit.

## Constraints

- NEVER modify the target project's source code
- NEVER sync without user approval at the plan gate
- In push mode, preserve one state entry per target path and update it only after success
- In pull mode, always clean up the temporary clone, even on failure

## Target Path

<target-path>$ARGUMENTS</target-path>
