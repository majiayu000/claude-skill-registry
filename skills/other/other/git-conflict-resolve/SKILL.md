---
name: git-conflict-resolve
version: 1.0.0
description: '[Git] Resolve git merge/cherry-pick/rebase conflicts with backup, analysis, and reporting'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/evidence-based-reasoning-protocol.md`

## Quick Summary

**Goal:** Resolve git merge/cherry-pick/rebase conflicts with backup, analysis, and structured reporting.

**Workflow:**
1. **Backup** — Create safety backup of current state
2. **Analyze** — Identify conflict types and affected files
3. **Resolve** — Apply resolution strategy per conflict
4. **Report** — Generate conflict resolution report

**Key Rules:**
- Always create backup before resolving conflicts
- Prefer preserving both sides' intent over arbitrary choice
- Generate resolution report for audit trail

## Purpose

Systematically resolve git conflicts (merge, cherry-pick, rebase) with:

1. Backup of all conflicted files before resolution
2. Per-file conflict analysis with root cause explanation
3. Resolution with documented rationale
4. Comprehensive report generation

## Variables

OPERATION: auto-detect (cherry-pick, merge, rebase) from git state
REPORT_PATH: `plans/reports/conflict-resolution-{date}-{operation}-{source}.md`
BACKUP_PATH: `.ai/workspace/conflict-backups-{date}/`

## Workflow

### Step 1: Detect conflict state

```bash
# Detect operation type
git status  # Check for "cherry-pick in progress", "merge in progress", etc.

# List all conflicted files
git diff --name-only --diff-filter=U  # Unmerged files (both modified)
git status --short | grep "^DU\|^UD\|^UU\|^AA\|^DD"  # All conflict types
```

Classify each conflict:

- **DU (Deleted by us):** File exists on source but not on target branch
- **UD (Deleted by them):** File exists on target but deleted by source
- **UU (Both modified):** Both branches modified the same file
- **AA (Both added):** Both branches added a file at the same path
- **DD (Both deleted):** Both branches deleted the file

### Step 2: Create backup files

**MANDATORY before any resolution.**

```bash
mkdir -p {BACKUP_PATH}

# For each conflicted file, copy WITH conflict markers preserved
cp <conflicted-file> {BACKUP_PATH}/<filename>.conflict
```

Create a TaskCreate item for each conflicted file PLUS report and review tasks.

### Step 3: Analyze each conflict (per file)

For each conflicted file, perform this analysis:

#### 3a. Understand the conflict type

- **DU/UD (deleted by one side):** Check if the file was introduced in a commit not present on the target branch. Read the file content from the source commit to understand what it provides.
- **UU (both modified):** Read the conflict markers. Identify what each side changed and why.

#### 3b. Read both versions

```bash
# For UU conflicts: read the file with conflict markers
# Look for <<<<<<< HEAD / ======= / >>>>>>> markers

# For DU conflicts: get the source version
git show <source-commit>:<file-path>

# Optionally extract clean versions
git show HEAD:<file-path> > {BACKUP_PATH}/<filename>.ours
git show <source-commit>:<file-path> > {BACKUP_PATH}/<filename>.theirs
```

#### 3c. Analyze dependencies

- **Check callers:** Do other files reference methods/classes in this file? Are caller names compatible?
- **Check constructor/DI:** Does the resolution require new dependencies?
- **Check cross-file consistency:** Will the resolution break other files?

#### 3d. Determine resolution strategy

| Conflict Pattern                                       | Resolution Strategy                                |
| ------------------------------------------------------ | -------------------------------------------------- |
| DU: File needed by feature                             | Accept theirs (add the file)                       |
| DU: File not needed                                    | Keep ours (skip the file)                          |
| UU: Non-overlapping changes                            | Merge both (keep all changes)                      |
| UU: Overlapping, source modifies methods not on target | Keep ours if methods don't exist on target         |
| UU: Overlapping, both modify same method               | Manual merge with careful analysis                 |
| UU: Schema/snapshot files                              | Accept theirs for new entities, merge for modified |

### Step 4: Resolve each conflict

Apply the determined strategy:

```bash
# Accept theirs (source version)
git checkout --theirs <file> && git add <file>

# Keep ours (target version)
git checkout --ours <file> && git add <file>

# Manual merge: Edit the file to remove conflict markers, then:
git add <file>
```

For manual merges:

1. Remove `<<<<<<< HEAD`, `=======`, `>>>>>>> <commit>` markers
2. Keep the correct content from each side
3. Verify no leftover conflict markers: `git diff --check`

### Step 5: Verify resolution

```bash
# Check no unmerged files remain
git diff --name-only --diff-filter=U

# Check no leftover conflict markers
git diff --check

# Review overall status
git status
```

### Step 6: Complete the operation

```bash
# For cherry-pick
git cherry-pick --continue --no-edit

# For merge
git commit  # (merge commit is auto-prepared)

# For rebase
git rebase --continue
```

### Step 7: Generate report

Create a comprehensive report at `{REPORT_PATH}` with:

1. **Header:** Date, source commit/branch, target branch, result commit
2. **Summary:** Total conflicts, categories, overall risk
3. **Per-file details:**
    - File path
    - Conflict type (DU/UU/etc.)
    - Root cause (why the conflict occurred)
    - Resolution chosen (accept theirs/keep ours/manual merge)
    - Rationale (why this resolution was chosen)
    - Risk level (Low/Medium/High)
4. **Summary table:** All files with conflict type, resolution, risk
5. **Root cause analysis:** Common patterns across conflicts
6. **Recommendations:** Follow-up actions, build verification, etc.

### Step 8: Final review

- Verify report is complete and accurate
- Check that all backup files exist
- Confirm build passes (if applicable)
- Flag any Medium/High risk resolutions for user attention

## Resolution Decision Framework

### When to "Accept Theirs" (source version)

- File is NEW (DU) and required by the feature being cherry-picked/merged
- File contains schema/config additions needed by new entities
- Source has strictly more content (e.g., empty class → populated class)

### When to "Keep Ours" (target version)

- Source modifies methods that don't exist on target (added by uncommitted prerequisite)
- Source renames methods/types that target callers still reference by old names
- Changes are not required for the feature being brought in

### When to "Manual Merge"

- Both sides have legitimate changes that need to coexist
- Schema files where both add new entries (keep both)
- Config files where both add new sections

### Risk Assessment

| Risk       | Criteria                                       | Action                                       |
| ---------- | ---------------------------------------------- | -------------------------------------------- |
| **Low**    | New file, no existing code affected            | Proceed                                      |
| **Medium** | Method changes, caller compatibility uncertain | Flag in report, recommend build verification |
| **High**   | Breaking changes, cross-service impact         | Require user confirmation before proceeding  |

## Notes

- Always create backup files BEFORE any resolution
- Never force-resolve without understanding the root cause
- For complex conflicts (>3 conflict regions in one file), extract both clean versions for side-by-side analysis
- Check for prerequisite commits: if a cherry-pick modifies files from prior commits not on target, note this in the report
- Use `git diff <commit>^..<commit> -- <file>` to see the actual diff of a specific commit (not the full file state)

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
