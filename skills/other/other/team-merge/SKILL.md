---
description: Merge completed parallel agent work and trigger GitHub sync per increment. Activates for: team merge, merge agents, combine work, team finish.
---

# Team Merge

**Verify all teammates completed, run quality gates, close increments, and trigger sync.**

## Usage

```bash
/sw:team-merge
/sw:team-merge --dry-run            # Preview merge plan
/sw:team-merge --skip-sync          # Merge without GitHub/JIRA sync
```

## What This Skill Does

1. **Verify all teammates completed** -- block if any are still running
2. **Run quality gates per domain** -- `/sw:grill` for each increment
3. **Close increments in dependency order** -- `/sw:done` per increment
4. **Trigger sync** -- pushes to GitHub (`/sw-github:sync`) or JIRA (`/sw-jira:push`)

## Workflow

### Step 1: Pre-flight Check

Native Agent Teams share the filesystem, so verification is straightforward:

```
For each teammate's increment:
  - Check tasks.md is 100% complete
  - Verify /sw:grill quality gate passed
  - If any teammate still running -> report and ask user to wait
```

### Step 2: Validate Repository Structure

For multi-repo team sessions, verify all agent work follows the repository directory convention:

```bash
# Check for repos created outside repositories/ directory
if [ -d "repositories" ]; then
  for git_dir in ./*/.git; do
    repo_name=$(dirname "$git_dir")
    if [[ "$repo_name" != ./repositories/* && "$repo_name" != "./.git" ]]; then
      echo "WARNING: Repository $repo_name found outside repositories/ directory"
      echo "Expected: repositories/{org}/$(basename $repo_name)/"
    fi
  done
fi
```

If repos are found outside `repositories/`, report as a warning with remediation instructions. The merge proceeds but the report flags the issue for cleanup.

### Step 3: Determine Closure Order

Dependencies flow: shared -> backend -> frontend (or as defined by team topology)

```
Closure order respects contract chain:
1. shared/types (no dependencies)
2. database (depends on shared types)
3. backend (depends on database + shared)
4. frontend (depends on backend API + shared types)
5. devops/qa/security (independent, close last)
```

### Step 4: Close Each Increment

For each teammate's increment, in dependency order:

```bash
# Run /sw:done --auto per increment -- triggers quality gates, skips user confirmation
/sw:done <increment-id> --auto
```

This ensures:
- `/sw:grill` runs for each increment
- `tasks.md` and `spec.md` ACs are validated
- `metadata.json` is updated to `completed`
- Living docs are generated

### Step 5: Trigger Sync

For each closed increment, trigger external sync:

```bash
# GitHub Issues sync
/sw-github:sync <increment-id>

# JIRA sync (if configured)
/sw-jira:push <increment-id>
```

### Step 6: Clean Up

- Signal team completion
- Archive completed increments if configured

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Show merge plan without executing |
| `--skip-sync` | Merge without triggering GitHub/JIRA sync |
| `--skip-done` | Skip running /sw:done (increments stay active) |

## Example

```
User: /sw:team-merge

Checking teammates...
  backend (0301-api-endpoints)   -- done, grill passed
  frontend (0302-ui-components)  -- done, grill passed
  shared (0300-shared-types)     -- done, grill passed

Closure order: 0300 -> 0301 -> 0302

Running /sw:done 0300-shared-types...      done
Running /sw:done 0301-api-endpoints...     done
Running /sw:done 0302-ui-components...     done

Syncing to GitHub...
  0300 -> issue #45 closed
  0301 -> issue #46 closed
  0302 -> issue #47 closed

All increments merged and synced.
```
