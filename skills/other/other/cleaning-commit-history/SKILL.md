---
name: cleaning-commit-history
description: Reorganize and clean up messy commit history on a feature branch into logical, reviewable commits. Use when cleaning up commits, preparing a branch for review, separating formatting from logic changes, fixing broken intermediate states, or squashing WIP commits.
context: fork
---

# Cleaning Commit History

Clean up messy git histories into logical commit sequences that are easy to review and maintain.

## VCS Detection

Check which VCS to use first:

```bash
jj root 2>/dev/null && echo "USE_JJ=true" || echo "USE_JJ=false"
```

If jj is available, prefer jj commands -- they're non-interactive and the oplog provides automatic safety (no manual backup branch needed).

## Operating Procedure

### Phase 0: Safety

**Git**: Create backup branch before any surgery:

```bash
git branch ${CURRENT_BRANCH}-backup
```

**jj**: Not needed -- oplog provides safety. Note the current operation ID with `jj op log -n 1`.

### Phase 1: Inventory

1. Determine base branch (main, master, or dev)
2. Use `git merge-base` (or `jj log`) to find comparison point
3. Inventory all feature-only changes with `git log --oneline $BASE..$FEATURE_BRANCH`
4. Note large files, generated paths, vendored code, migrations

### Phase 2: Sea of Changes

Compute the net diff from BASE to FEATURE_BRANCH (not commit-by-commit). This represents all changes that need reorganization.

### Phase 3: Classify & Cluster

Cluster changes into logical buckets (strict priority):

1. **Generated/Vendored/Lockfiles** -- isolated to dedicated commits
2. **Pure renames/moves** -- separated from content changes
3. **Formatting-only** (whitespace, import order, lint fixes) -- isolated
4. **Refactors without behavior change** -- separate from logic
5. **Feature/Logic changes** -- grouped by cohesive unit
6. **Tests** -- co-located with their corresponding logic changes

**Split** when a commit mixes mechanical and semantic changes. **Squash** when multiple tiny edits serve the same concern.

### Phase 4: Determine Commit Order

Order for buildability and minimal noise:

1. Pure renames/moves
2. Formatting-only sweep
3. Refactors (non-behavioral)
4. Schema/Migrations
5. Feature/Logic in dependency order
6. Tests (accompany or immediately follow their logic)
7. Docs/Changelog
8. Vendored/lockfile updates

Every intermediate state must build and pass tests.

### Phase 5: Rebuild Commits

**Git**: `git reset --mixed $BASE`, then stage related hunks per planned commit with `git add -p`.

**jj workflow**:

```bash
# Squash related changes (always use -m!)
jj squash --from <change1> --into <change2> -m "combined message"

# Selective restore (jj split is interactive, avoid it)
jj new -m "first part"
jj restore --from @- <files-for-first-commit>

# Reorder
jj rebase -r <change> -d <new-parent>

# Clean up messages
jj describe -m "feat(scope): message"

# If anything goes wrong
jj op restore <before-surgery>
```

### Phase 6: Validation

- `git diff $BASE..HEAD` equals the original sea (no loss of intent)
- Each commit shows clean boundaries with minimal file overlap
- Every commit builds and tests successfully
- No secrets or large binary blobs

## Commit Message Style

```text
<type>(<scope>): <short description in present tense, under 72 chars>

- <Bullet point starting with verb>
- <What changed and why>

[Optional: BREAKING CHANGE:, Refs:, Co-authored-by:]
```

Types: feat, fix, refactor, perf, chore, test, docs, build, ci

## Strict Rules

- **Never** mix formatting/import-order with behavior changes
- **Always** separate file renames/moves from edits to those files
- **Always** keep generated and vendored changes isolated
- **Always** co-locate tests with their logic change
- **Never** create broken intermediate states

## Deliverables

1. **Safety Confirmation**: Backup branch (git) or oplog snapshot (jj)
2. **Commit Plan**: Ordered list with title, scope, type, rationale, and files
3. **Applied History**: Rewritten commits matching the plan
4. **Summary Report**: Changes vs original, tradeoffs, recovery instructions
