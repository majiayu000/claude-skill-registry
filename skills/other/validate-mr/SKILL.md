---
name: validate-mr
description: Use when you need a diff-derived test plan for an MR — reads the
  diff, groups changes by area, runs targeted verifications, and proves
  revert-tests are genuine guards, not dead assertions.
alwaysApply: false
category: validation
tags:
- pr
- mr
- validation
- test-plan
- diff
- revert-test
- evidence
tools: []
usage_patterns:
- diff-derived-test-plan
- revert-test-quality-check
- evidence-capture
complexity: intermediate
model_hint: standard
estimated_tokens: 650
progressive_loading: false
dependencies:
- leyline:git-platform
- imbue:proof-of-work
role: entrypoint
---

# validate-mr: Diff-Derived Test Plan

Generate and self-execute a validation plan matched to what actually changed
in an MR. Replaces generic "tests pass" with area-targeted evidence and
revert-test quality checks that prove tests catch regressions.

## When To Use

- End of `/fix-pr` Step 5 (Validate), before Step 6 (Complete)
- Standalone after any MR fix, to generate targeted validation evidence
- When you need proof that revert-tests are genuine guards

## When NOT To Use

- `--scope minor` with only formatting or doc changes (no logic changed)
- No diff available (clean branch, nothing changed)
- `--skip-validate` passed to `/fix-pr`

## Algorithm

```
fetch diff -> group by area -> generate steps -> execute -> revert-test -> table
```

## Step 1: Fetch Diff and Detect Areas

```bash
# Get changed file list from the MR
MR_NUMBER=<number from invocation or current branch>
CHANGED=$(gh pr diff "$MR_NUMBER" --name-only)
# Fallback when no MR number:
# CHANGED=$(git diff "origin/$(git rev-parse --abbrev-ref HEAD@{upstream})...HEAD" \
#   --name-only 2>/dev/null)
```

Group changed files into areas using ripgrep (grep if rg unavailable):

```bash
RUST_FILES=$(echo "$CHANGED"  | rg '\.rs$|Cargo\.(toml|lock)$' || true)
PY_FILES=$(echo "$CHANGED"    | rg '\.py$|pyproject\.toml$|requirements.*\.txt$' || true)
SH_FILES=$(echo "$CHANGED"    | rg '\.sh$|\.githooks' || true)
GRAMMAR_FILES=$(echo "$CHANGED" | rg '\.(lark|peg|g4)$' || true)
```

Area routing table:

| Area | File patterns | Verification type |
|------|---------------|-------------------|
| Rust | `*.rs`, `Cargo.toml`, `Cargo.lock` | cargo build + per-crate test |
| Python | `*.py`, `pyproject.toml` | pytest per changed module |
| Shell | `*.sh`, `.githooks/*` | shellcheck |
| Grammar | `*.lark`, `*.peg`, `*.g4` | language-specific lint |
| Build/config | `*.yaml`, `*.json`, `*.toml` | parse check |

## Step 2: Generate and Execute Steps per Area

For each non-empty area, generate and run at least one verification step.
Assign `[E1]`, `[E2]`, ... labels to each captured output.

### Rust

```bash
# Build with default features
cargo build --workspace 2>&1
# Evidence: [En] → "0 errors, 0 warnings"

# Build with --all-features
cargo build --workspace --all-features 2>&1
# Evidence: [En+1]

# Per-crate test for each changed crate
# Extract crate directory from changed path, e.g. crates/token-types/src/lib.rs
CHANGED_CRATES=$(echo "$RUST_FILES" \
  | rg -o '(?:crates|src)/[^/]+' \
  | sort -u \
  | xargs -I{} basename {})
for CRATE in $CHANGED_CRATES; do
  cargo test -p "$CRATE" 2>&1
done
```

### Python

```bash
# Targeted test per changed module
for PY_FILE in $PY_FILES; do
  MODULE=$(basename "${PY_FILE%.py}")
  TEST_FILE="tests/test_${MODULE}.py"
  if [[ -f "$TEST_FILE" ]]; then
    uv run pytest "$TEST_FILE" -v 2>&1
  fi
done

# Or project-specific runner if Makefile target exists
make test 2>&1 || uv run pytest tests/ -v 2>&1
```

### Shell

```bash
for SH_FILE in $SH_FILES; do
  [[ -f "$SH_FILE" ]] && shellcheck "$SH_FILE" 2>&1
done
```

### Build/config parse check

```bash
# YAML files
for YML in $(echo "$CHANGED" | rg '\.ya?ml$' || true); do
  [[ -f "$YML" ]] && python3 -c "import yaml; yaml.safe_load(open('$YML'))" \
    && echo "PASS: $YML" || echo "FAIL: $YML"
done

# JSON files
for JSON_F in $(echo "$CHANGED" | rg '\.json$' || true); do
  [[ -f "$JSON_F" ]] && python3 -m json.tool "$JSON_F" > /dev/null \
    && echo "PASS: $JSON_F" || echo "FAIL: $JSON_F"
done
```

## Step 3: Revert-Test Quality Check

Prove at least one test is a genuine guard, not a dead assertion.

**Safety: abort if the working tree has uncommitted changes.**

```bash
if ! git diff --exit-code > /dev/null 2>&1; then
  echo "[RT] SKIP: working tree dirty — revert-test unsafe"
  # Mark INCONCLUSIVE and continue
fi
```

**Algorithm (one representative fix):**

1. From the changed source files, find one that has a corresponding test.
   - Rust: a `#[test]` in the same crate that exercises a changed function.
   - Python: `tests/test_<module>.py` for a changed `<module>.py`.
   - Shell: a test harness that invokes the changed script.
2. Identify the specific changed line or block from the diff.
3. Edit that line to revert the fix to its broken state.
4. Run the targeted test: confirm it **FAILS** (expected).
5. Restore: `git checkout — <file>` (git-based restore, safe on interrupt).
6. Run the targeted test again: confirm it **PASSES**.
7. If any step cannot complete, mark INCONCLUSIVE with the reason.

**Revert-test output format:**

```
[RT-1] Target: <file>:<line> — <description of fix>
[RT-2] Broke fix: <edit description>
[RT-3] Ran: <test command> → <test name> FAILED (expected)
[RT-4] Restored: git checkout -- <file>
[RT-5] Ran: <test command> → <test name> PASSED
Result: PASS — test is a genuine guard
```

**When no covering test exists:**

```
Revert-test: INCONCLUSIVE — no covering test for <changed area>
Recommendation: add a test for <changed function or behaviour>
```

## Step 4: Final Full-Suite Run

After all area checks and the revert-test:

```bash
# Rust workspace
cargo test --workspace 2>&1

# Python project
uv run pytest tests/ -v 2>&1

# Mixed project: run both
cargo test --workspace 2>&1 && uv run pytest tests/ -v 2>&1
```

Capture full output as final evidence `[En]`.

## Step 5: Produce Summary Table

```markdown
### validate-mr: <MR title or number>

| Area | Step | Evidence | Result |
|------|------|----------|--------|
| Rust: token-types | cargo build --workspace | [E1] 0 errors | PASS |
| Rust: token-types | cargo test -p token-types | [E2] 12 passed | PASS |
| Rust: token-types | cargo build --all-features | [E3] 0 errors | PASS |
| Shell: hooks/pre-commit | shellcheck | [E4] 0 issues | PASS |
| Revert-test: lib.rs:45 | break/fail/restore | [RT-1..5] genuine guard | PASS |
| Final: cargo test --workspace | full suite | [E5] 694 passed, 0 failed | PASS |

**Totals**: 6 steps — 6 PASS, 0 FAIL, 0 INCONCLUSIVE
```

## Step 6: Posting (--post flag only)

When `--post` is given, post the summary table as a PR comment:

```bash
gh pr comment "$MR_NUMBER" --body "$(cat /tmp/validate-mr-summary.md)"
```

Skip posting when invoked from `/fix-pr` — results feed into the Gate 3
summary comment instead.

## Failure Behaviour

When any step produces **FAIL**:

- Surface the failures in the summary table with the evidence reference.
- When called from `/fix-pr`: halt before Step 6 (Complete). The user must
  fix the failures or pass `--skip-validate` to `/fix-pr` to bypass.
- When called standalone: report failures and exit with non-zero status.

INCONCLUSIVE results are reported but do not halt the workflow.

## Exit Criteria

- [ ] `gh pr diff --name-only` returned a non-empty file list (diff fetched)
- [ ] Every detected area has at least one row in the summary table
- [ ] Every row shows an Evidence reference (`[E1]`, `[E2]`, etc.) with the
  actual command output, not fabricated
- [ ] Revert-test attempted for at least one area with a covering test, or
  documented as INCONCLUSIVE with reason
- [ ] Final full-suite run appears in the summary table
- [ ] Summary table is present with columns: Area, Step, Evidence, Result
- [ ] Any FAIL result halts `/fix-pr` before Step 6 when called from fix-pr
- [ ] Working tree is clean after skill completes (git checkout restore
  confirmed successful for any revert-test mutation)
