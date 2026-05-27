---
name: fix-llm-artifacts
description: Applies fixes from a prior review-llm-artifacts run, with safe/risky classification. Respects verify-llm-artifacts output when present to skip false positives.
disable-model-invocation: true
---

# Fix LLM Artifacts

Apply fixes from a previous `review-llm-artifacts` run with automatic safe/risky classification. If `.beagle/llm-artifacts-verification.json` exists, **skip** findings marked `false_positive` and treat `inconclusive` like risky fixes (prompt or skip per user).

## Usage

```
/beagle-core:fix-llm-artifacts [--dry-run] [--all] [--category <name>]
```

**Flags:**
- `--dry-run` - Show what would be fixed without changing files
- `--all` - Fix entire codebase (runs `review-llm-artifacts --all` first if no review JSON)
- `--category <name>` - Only fix specific category: `tests|dead-code|abstraction|style`

## Instructions

### Hard gates

Sequence matters. Do not apply fixes until each **pass condition** is satisfied (these steps are not “internal verification”).

1. **Working tree** — `git status --porcelain` is empty **or** a stash was created with message `beagle-core: pre-fix-llm-artifacts backup` and `git stash list` shows it. If the user refuses stash/backup, **stop** or document explicit acceptance of risk in the report before edits.
2. **Review artifact on disk** — `.beagle/llm-artifacts-review.json` exists, **or** `--all` completed a `review-llm-artifacts` run that wrote that file. Otherwise **stop** (no fixes from memory or guesses).
3. **Stale review** — If `jq -r '.git_head' .beagle/llm-artifacts-review.json` ≠ `git rev-parse HEAD`, prompt to re-run review. **`y`** → re-run review, then continue. **`n`** → **abort** the fix pass (do not apply fixes against stale findings).
4. **Verification overlay** — If `.beagle/llm-artifacts-verification.json` exists, it must **parse**; build exclude/inconclusive sets **before** partitioning (Section 4). On parse failure, **stop** and report the error.
5. **Risky fixes** — No `code_removal`, `logic_change`, `mock_boundary`, `abstraction_change`, or `test_refactor` work without the interactive choice in Section 6 (or `s` to skip all remaining risky items).

**Post-edit:** Sections 7–8 **pass** only when invoked tools exit successfully (non-zero = failure; keep JSON artifacts per Cleanup).

### 1. Parse Arguments

Extract flags from `$ARGUMENTS`:
- `--dry-run` - Preview mode only
- `--all` - Full codebase scan
- `--category <name>` - Filter to specific category

### 2. Pre-flight Safety Checks

```bash
# Check for uncommitted changes
git status --porcelain
```

If working directory is dirty, warn:
```
Warning: You have uncommitted changes. Creating a git stash before proceeding.
Run `git stash pop` to restore if needed.
```

Create stash if dirty:
```bash
git stash push -m "beagle-core: pre-fix-llm-artifacts backup"
```

### 3. Load Review Results

Check for existing review file:
```bash
cat .beagle/llm-artifacts-review.json 2>/dev/null
```

**If file missing:**
- If `--all` flag: Run `review-llm-artifacts --all` first to produce a full-project review
- Otherwise: Fail with: "No review results found. Run `/beagle-core:review-llm-artifacts` first."

**Optional verification overlay** — if `.beagle/llm-artifacts-verification.json` exists:
- Build a set of finding ids with `status: false_positive` → **exclude** these from all fix lists.
- Finding ids with `status: inconclusive` → **always** follow risky-fix handling (Section 6), even if `fix_safety` was `Safe` in the review.
- Finding ids with `status: confirmed_issue` → use review JSON `fix_safety` / `risk` as usual.

If verification is missing, warn when applying deletes or `dead-code` fixes: "For fewer false positives, run `/beagle-core:verify-llm-artifacts` first."

**If file exists, validate freshness:**
```bash
# Get stored git HEAD, scope, and target from JSON
stored_head=$(jq -r '.git_head'   .beagle/llm-artifacts-review.json)
stored_scope=$(jq -r '.scope // "all"'  .beagle/llm-artifacts-review.json)
stored_target=$(jq -r '.target // "."'  .beagle/llm-artifacts-review.json)
current_head=$(git rev-parse HEAD)

if [ "$stored_head" != "$current_head" ]; then
  echo "Warning: Review was run at commit $stored_head, but HEAD is now $current_head"
fi
```

If stale, prompt: "Review results are stale. Re-run review? (y/n)".
- **`y`** → **re-run `review-llm-artifacts` with the original scope and target** read from the stale JSON, then reload. This preserves the user's original intent; do **not** silently widen or narrow the scope, which would apply fixes unrelated to the user's diff (or miss files they cared about). Concretely:
  - `scope == "changed"` → invoke `review-llm-artifacts "$stored_target"` (default scope is already changed-files).
  - `scope == "all"`     → invoke `review-llm-artifacts --all "$stored_target"`.
  - If `scope` or `target` is missing from the JSON (pre-schema review), **do not abort.** Assume `scope = "all"` and `target = "."`, then warn:
    > "Review JSON predates the scope/target schema; re-running as a full-project scan (`--all`). If you meant a narrower scope (the default changed-files diff, or a subdirectory), cancel now and re-run `/beagle-core:review-llm-artifacts` explicitly."
    Proceed only if the user does not cancel.
- **`n`** → **abort** (do not apply fixes; stale findings are not trustworthy).

### 4. Partition Findings by Safety

Parse findings from JSON and classify by `fix_safety` field (after applying verification overlay from step 3):

**Safe Fixes** (auto-apply):
- `unused_import` - Unused imports
- `todo_comment` - Stale TODO/FIXME comments
- `dead_code_obvious` - Obviously unreachable code
- `verbose_comment` - Overly verbose LLM-style comments
- `redundant_type` - Redundant type annotations

**Risky Fixes** (require confirmation):
- `test_refactor` - Test structure changes
- `abstraction_change` - Class/function extraction
- `code_removal` - Removing functional code
- `mock_boundary` - Test mock scope changes
- `logic_change` - Any behavioral modifications

### 5. Apply Safe Fixes

If `--dry-run`:
```markdown
## Safe Fixes (would apply automatically)

| File | Line | Type | Description |
|------|------|------|-------------|
| src/api.py | 15 | unused_import | Remove `from typing import List` |
| src/models.py | 42 | verbose_comment | Remove 23-line docstring |
...
```

Otherwise, spawn parallel agents per category with `Task` tool:

```
Task: Apply safe fixes for category "{category}"
Files: [list of files with findings in this category]
Instructions: Apply each fix, preserving surrounding code. Report success/failure per fix.
```

Categories to parallelize:
- `style` - Comments, formatting
- `dead-code` - Imports, unreachable code
- `tests` - Test-related safe fixes
- `abstraction` - Safe refactors

### 6. Handle Risky Fixes

For each risky fix, prompt interactively:

```
[src/services/auth.py:156] Remove seemingly unused authenticate_legacy() method?
This method has no callers in the codebase but may be used externally.
(y)es / (n)o / (s)kip all risky:
```

Track user choices:
- `y` - Apply this fix
- `n` - Skip this fix
- `s` - Skip all remaining risky fixes

### 7. Post-Fix Verification

Detect project type and run appropriate linters:

**Python:**
```bash
# Check if ruff config exists
if [ -f "pyproject.toml" ] || [ -f "ruff.toml" ]; then
    ruff check --fix .
    ruff format .
fi

# Check if mypy config exists
if [ -f "pyproject.toml" ] || [ -f "mypy.ini" ]; then
    mypy .
fi
```

**TypeScript/JavaScript:**
```bash
# Check for eslint
if [ -f "eslint.config.js" ] || [ -f ".eslintrc.json" ]; then
    npx eslint --fix .
fi

# Check for TypeScript
if [ -f "tsconfig.json" ]; then
    npx tsc --noEmit
fi
```

**Go:**
```bash
if [ -f "go.mod" ]; then
    go vet ./...
    go build ./...
fi
```

### 8. Run Tests

```bash
# Python
if [ -f "pyproject.toml" ] || [ -f "pytest.ini" ]; then
    pytest
fi

# JavaScript/TypeScript
if [ -f "package.json" ]; then
    npm test 2>/dev/null || yarn test 2>/dev/null || true
fi

# Go
if [ -f "go.mod" ]; then
    go test ./...
fi
```

### 9. Report Results

```markdown
## Fix Summary

### Applied Fixes
- [x] src/api.py:15 - Removed unused import `List`
- [x] src/models.py:42-64 - Removed verbose docstring
- [x] src/auth.py:156-189 - Removed dead method (user confirmed)

### Skipped Fixes
- [ ] src/services/cache.py:23 - User declined risky fix
- [ ] tests/test_api.py:45 - Test refactor skipped

### Verification Results
- Linter: PASSED
- Type check: PASSED
- Tests: PASSED (42 passed, 0 failed)

### Diff Summary
```bash
git diff --stat
```

## Cleanup

On successful completion (all verifications pass):
```bash
rm -f .beagle/llm-artifacts-review.json .beagle/llm-artifacts-verification.json
```

If any verification fails, keep the files and report:
```
Review file preserved at .beagle/llm-artifacts-review.json
Fix issues and re-run, or restore with: git stash pop
```

## Example

```bash
# Preview all fixes without applying
/beagle-core:fix-llm-artifacts --dry-run

# Fix only dead code issues
/beagle-core:fix-llm-artifacts --category dead-code

# Full codebase scan and fix
/beagle-core:fix-llm-artifacts --all

# Fix style issues only, preview first
/beagle-core:fix-llm-artifacts --category style --dry-run
```
