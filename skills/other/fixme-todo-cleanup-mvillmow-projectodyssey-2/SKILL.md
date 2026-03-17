# FIXME/TODO Cleanup Skill

| Field | Value |
|-------|-------|
| Date | 2026-01-01 |
| Objective | Systematically resolve all FIXME/TODO items in a directory |
| Outcome | 7 PRs merged, 3 issues closed |
| Category | debugging |

## When to Use

- User requests cleanup of FIXME/TODO items across a codebase
- Technical debt reduction initiative
- Pre-release code quality sweep
- Issue tracking consolidation

## Verified Workflow

### 1. Discovery Phase

```bash
# Find all FIXME/TODO items
grep -rn "FIXME\|TODO" shared/ --include="*.mojo"
```

### 2. Categorization

Group items by:

- **Stale references**: FIXME pointing to closed issues
- **Missing implementations**: Placeholder code needing real logic
- **External blockers**: Items blocked by language/compiler features
- **Documentation**: TODO in docs describing future work

### 3. Execution Pattern

For each actionable item:

```bash
# 1. Create branch from latest main
git checkout main && git pull origin main
git checkout -b <issue-number>-<description>

# 2. Make the fix (one FIXME per commit)

# 3. Validate
just pre-commit-all
pixi run mojo test tests/

# 4. Commit with issue reference
git add . && git commit -m "fix(scope): description

Closes #<issue>"

# 5. Push and create PR with auto-merge
git push -u origin <branch-name>
gh pr create --body "Closes #<issue>"
gh pr merge --auto --rebase
```

### 4. Handle Flaky CI

```bash
# Retry failed jobs
gh run rerun <run-id> --failed
```

## Failed Attempts

### 1. `@value` to `@fieldwise_init` Migration

**What was tried**: Replace deprecated `@value` decorator with `@fieldwise_init`

**Error**:

```mojo
error: 'TrainingCallbacks' has an explicitly declared fieldwise initializer
```

**Why it failed**: `@fieldwise_init` generates an `__init__` method, conflicting with custom `__init__`

**Solution**: Remove decorator entirely, keep explicit `Copyable, Movable` conformances:

```mojo
# Before (broken)
@fieldwise_init
struct TrainingCallbacks(Copyable, Movable):
    fn __init__(out self, verbose: Bool = True):
        self.verbose = verbose

# After (working)
struct TrainingCallbacks(Copyable, Movable):
    var verbose: Bool

    fn __init__(out self, verbose: Bool = True):
        self.verbose = verbose
```

### 2. Ralph-Loop Hook Stuck

**What was tried**: Set `active: false` in ralph-loop.local.md

**Why it failed**: Hook continued firing despite deactivation flag

**Solution**: Delete the file entirely:

```bash
rm .claude/ralph-loop.local.md
```

## Results & Parameters

### Items Resolved

| PR | Issue | Description |
|----|-------|-------------|
| #3035 | - | Update stale issue references |
| #3036 | #3031 | Remove MXFP4 FIXME |
| #3037 | #3033 | Implement conftest fixtures |
| #3038 | #3034 | Implement script_runner |
| #3039 | #3034 | Implement dataset_loaders |
| #3040 | #3034 | Export script utilities |
| #3041 | #3032 | Update ExTensor Array API |

### Items NOT Resolved (External Blockers)

| File | Line | Blocker |
|------|------|---------|
| profiling.mojo | 650 | Mojo FileIO stability |
| logging.mojo | 442 | Mojo env var support |
| mixed_precision.mojo | 284, 368 | Compiler SIMD FP16 support |
| training/\_\_init\_\_.mojo | 412 | Track 4 Python data loader |
| trainer_interface.mojo | 392 | Track 4 Python data loader |

### Git Configuration

```yaml
branch_naming: "<issue-number>-<description>"
commit_format: "type(scope): description\n\nCloses #<issue>"
merge_strategy: "rebase"
auto_merge: true
```

## Key Learnings

1. **Categorize first**: Not all FIXME/TODO items are actionable - some are blocked by external dependencies
2. **One PR per fix**: Keeps changes atomic and reviewable
3. **Auto-merge is essential**: Reduces manual intervention for straightforward fixes
4. **Retry flaky tests**: Some CI tests are non-deterministic - retry before investigating
5. **Mojo decorator conflicts**: `@fieldwise_init` cannot coexist with custom `\_\_init\_\_`
