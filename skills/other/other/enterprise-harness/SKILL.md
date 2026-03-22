---
name: enterprise-harness
description: "Orchestrator-facing mechanical gate with 10 checks. Runs after builder returns code, before merge. Builder cannot see or game these checks. Produces PASS/FAIL verdict with exact failure details. Use as the final quality gate before shipping."
---

# Enterprise Harness

Orchestrator-only quality gate. Runs AFTER a builder agent returns code, BEFORE merge/cherry-pick. The builder never sees these checks and cannot game them.

## Prerequisites

## STACK RESOLUTION

Read `.claude/enterprise-state/stack-profile.json` at skill start. Extract:
- `$TEST_CMD` = `commands.test_all`
- `$BUILD_CMD` = `commands.build_frontend`
- `$SOURCE_DIR` = `structure.source_dirs.backend`
- `$FRONTEND_DIR` = `structure.source_dirs.frontend`
- `$FILE_EXTENSIONS` = `conventions.file_extensions`

If no profile exists: BLOCKED — run /enterprise-discover first.

Before running, collect:
- `TASK_SLUG` — the task identifier (e.g., `sticky-notes-kanban`, `placeholder-products`)
- `BRANCH` — the builder's feature branch
- `BASE` — the base branch to diff against (usually `dev` or `main`)

Determine changed files once and reuse throughout:

```bash
CHANGED_FILES=$(git diff --name-only $BASE...$BRANCH)
CHANGED_JS=$(echo "$CHANGED_FILES" | grep -E "\.($(echo "$FILE_EXTENSIONS" | tr ',' '|'))$" || true)
CHANGED_TEST_FILES=$(echo "$CHANGED_JS" | grep -E '(__tests__|\.test\.|\.spec\.)' || true)
CHANGED_SRC_FILES=$(echo "$CHANGED_JS" | grep -vE '(__tests__|\.test\.|\.spec\.)' || true)
CHANGED_FRONTEND=$(echo "$CHANGED_FILES" | grep "^$FRONTEND_DIR/" || true)
```

---

## The 10 Checks

Run each check sequentially. Record PASS, FAIL, or WARN for each. Stop-on-first-FAIL is NOT used — run all 10 to give the builder a complete list.

---

### CHECK 1: Contract Exists

A contract file must exist for the task.

```bash
CONTRACT=$(ls docs/contracts/*${TASK_SLUG}* 2>/dev/null)
if [ -z "$CONTRACT" ]; then
  echo "FAIL — no contract found matching *${TASK_SLUG}* in docs/contracts/"
else
  echo "PASS — $CONTRACT"
fi
```

FAIL if no contract file found.

---

### CHECK 2: Tests Per Postcondition

Every postcondition in the contract must have at least one corresponding test.

```bash
# Count postconditions in contract
PC_COUNT=$(grep -cE '^[[:space:]]*-?\s*PC-' "$CONTRACT" 2>/dev/null || echo 0)

# Count test blocks in changed test files
TEST_COUNT=0
if [ -n "$CHANGED_TEST_FILES" ]; then
  TEST_COUNT=$(echo "$CHANGED_TEST_FILES" | xargs grep -cE '(^[[:space:]]*(it|test)\(|describe\()' 2>/dev/null | awk -F: '{s+=$NF} END {print s+0}')
fi

echo "Postconditions: $PC_COUNT | Tests: $TEST_COUNT"
if [ "$TEST_COUNT" -lt "$PC_COUNT" ]; then
  echo "FAIL — $TEST_COUNT tests < $PC_COUNT postconditions"
else
  echo "PASS"
fi
```

FAIL if test count < postcondition count.

---

### CHECK 3: Tests Pass

Run tests and compare against the main baseline to isolate new failures.

```bash
# Get baseline failures on BASE branch (if any)
git stash --quiet 2>/dev/null
git checkout "$BASE" --quiet 2>/dev/null
BASELINE_FAILURES=$($TEST_CMD --no-coverage --json 2>/dev/null | jq '.numFailedTests' 2>/dev/null || echo 0)
git checkout "$BRANCH" --quiet 2>/dev/null
git stash pop --quiet 2>/dev/null

# Run tests on builder's branch
TEST_OUTPUT=$($TEST_CMD --no-coverage --json 2>&1)
CURRENT_FAILURES=$(echo "$TEST_OUTPUT" | jq '.numFailedTests' 2>/dev/null || echo 999)

NEW_FAILURES=$((CURRENT_FAILURES - BASELINE_FAILURES))
if [ "$NEW_FAILURES" -gt 0 ]; then
  echo "FAIL — $NEW_FAILURES new test failure(s) introduced"
  # Show which tests failed
  echo "$TEST_OUTPUT" | jq -r '.testResults[] | select(.status=="failed") | .name' 2>/dev/null
else
  echo "PASS — no new failures (baseline: $BASELINE_FAILURES, current: $CURRENT_FAILURES)"
fi
```

FAIL if any new test failures introduced by the builder's changes.

---

### CHECK 4: Import Resolution

Every relative import in changed source files must resolve to an existing file.

```bash
IMPORT_FAILURES=0
IMPORT_DETAILS=""

if [ -n "$CHANGED_JS" ]; then
  while IFS= read -r file; do
    [ -z "$file" ] && continue
    DIR=$(dirname "$file")

    # Extract relative imports (require or import ... from)
    IMPORTS=$(grep -oE "(require\(['\"]\.\.?/[^'\"]+['\"]|from ['\"]\.\.?/[^'\"]+['\"])" "$file" 2>/dev/null | grep -oE '\.\.?/[^'\"]+' || true)

    while IFS= read -r imp; do
      [ -z "$imp" ] && continue
      RESOLVED="$DIR/$imp"

      # Check: exact path, .js, .jsx, /index.js, /index.jsx
      FOUND=0
      for EXT in "" ".js" ".jsx" "/index.js" "/index.jsx"; do
        if [ -f "${RESOLVED}${EXT}" ]; then
          FOUND=1
          break
        fi
      done

      if [ "$FOUND" -eq 0 ]; then
        IMPORT_FAILURES=$((IMPORT_FAILURES + 1))
        IMPORT_DETAILS="${IMPORT_DETAILS}\n  $file -> $imp (not found)"
      fi
    done <<< "$IMPORTS"
  done <<< "$CHANGED_JS"
fi

if [ "$IMPORT_FAILURES" -gt 0 ]; then
  echo "FAIL — $IMPORT_FAILURES unresolved import(s):$IMPORT_DETAILS"
else
  echo "PASS"
fi
```

FAIL if any relative import does not resolve to an existing file.

---

### CHECK 5: Data Shape Verification

Components must not read fields that don't exist in their data source.

```bash
SHAPE_FAILURES=0
SHAPE_DETAILS=""

if [ -n "$CHANGED_FRONTEND" ]; then
  CHANGED_COMPONENTS=$(echo "$CHANGED_FRONTEND" | grep -E '\.(jsx|js)$' | grep -v '__tests__' || true)

  while IFS= read -r comp; do
    [ -z "$comp" ] && continue

    # Find props destructuring from hooks (useQuery, useSearch, useState patterns)
    # Look for data.fieldName or result.fieldName access patterns
    ACCESSED_FIELDS=$(grep -oE '(data|result|response|item|row)\.[a-zA-Z_]+' "$comp" 2>/dev/null | sort -u || true)

    if [ -n "$ACCESSED_FIELDS" ]; then
      # Check if the component file also defines or receives these fields
      # Flag any field accessed on data/result objects that isn't defined in the same file
      # or in the API route/service that feeds it
      HOOK_CALLS=$(grep -oE 'use(Query|Mutation|Search|Fetch)\([^)]*\)' "$comp" 2>/dev/null || true)

      if [ -n "$HOOK_CALLS" ] && [ -n "$ACCESSED_FIELDS" ]; then
        # Extract API endpoint from hook call
        API_PATH=$(grep -oE "['\"]/api/[^'\"]*['\"]" "$comp" 2>/dev/null | head -1 | tr -d "'\"" || true)

        if [ -n "$API_PATH" ]; then
          # Find the route handler
          ROUTE_FILE=$(grep -rl "$API_PATH" $SOURCE_DIR/routes/ 2>/dev/null | head -1 || true)

          if [ -n "$ROUTE_FILE" ]; then
            while IFS= read -r field_access; do
              FIELD=$(echo "$field_access" | cut -d. -f2)
              # Check if field exists in route handler or its service
              if ! grep -q "$FIELD" "$ROUTE_FILE" 2>/dev/null; then
                SHAPE_FAILURES=$((SHAPE_FAILURES + 1))
                SHAPE_DETAILS="${SHAPE_DETAILS}\n  $comp accesses .$FIELD but not found in $ROUTE_FILE"
              fi
            done <<< "$ACCESSED_FIELDS"
          fi
        fi
      fi
    fi
  done <<< "$CHANGED_COMPONENTS"
fi

if [ "$SHAPE_FAILURES" -gt 0 ]; then
  echo "FAIL — $SHAPE_FAILURES data shape mismatch(es):$SHAPE_DETAILS"
else
  echo "PASS"
fi
```

FAIL if a component reads a field that the data source does not provide.

---

### CHECK 6: Build Passes (frontend only)

```bash
if [ -z "$CHANGED_FRONTEND" ]; then
  echo "SKIP — no frontend files changed"
else
  BUILD_OUTPUT=$(cd $FRONTEND_DIR && $BUILD_CMD 2>&1)
  BUILD_EXIT=$?

  if [ "$BUILD_EXIT" -ne 0 ]; then
    echo "FAIL — vite build exited $BUILD_EXIT"
    echo "$BUILD_OUTPUT" | tail -20
  else
    echo "PASS"
  fi
fi
```

FAIL if build exits non-zero. SKIP if no frontend files changed.

---

### CHECK 7: File Size Limits

Soft limit 400 lines (WARN), hard limit 800 lines (FAIL). Only checks files changed by the builder, not pre-existing legacy.

```bash
SIZE_FAIL=0
SIZE_WARN=0
SIZE_DETAILS=""

if [ -n "$CHANGED_SRC_FILES" ]; then
  while IFS= read -r file; do
    [ -z "$file" ] && continue
    [ ! -f "$file" ] && continue

    LINES=$(wc -l < "$file")

    # Check if file existed before the builder's changes
    EXISTED_BEFORE=$(git show "$BASE:$file" 2>/dev/null && echo "yes" || echo "no")

    if [ "$EXISTED_BEFORE" = "yes" ]; then
      OLD_LINES=$(git show "$BASE:$file" 2>/dev/null | wc -l)
      # Only flag if the builder made it worse
      if [ "$LINES" -gt 800 ] && [ "$OLD_LINES" -le 800 ]; then
        SIZE_FAIL=$((SIZE_FAIL + 1))
        SIZE_DETAILS="${SIZE_DETAILS}\n  FAIL: $file ($OLD_LINES -> $LINES lines, crossed 800 hard limit)"
      elif [ "$LINES" -gt 400 ] && [ "$OLD_LINES" -le 400 ]; then
        SIZE_WARN=$((SIZE_WARN + 1))
        SIZE_DETAILS="${SIZE_DETAILS}\n  WARN: $file ($OLD_LINES -> $LINES lines, crossed 400 soft limit)"
      fi
    else
      # New file created by builder
      if [ "$LINES" -gt 800 ]; then
        SIZE_FAIL=$((SIZE_FAIL + 1))
        SIZE_DETAILS="${SIZE_DETAILS}\n  FAIL: $file (new file, $LINES lines > 800 hard limit)"
      elif [ "$LINES" -gt 400 ]; then
        SIZE_WARN=$((SIZE_WARN + 1))
        SIZE_DETAILS="${SIZE_DETAILS}\n  WARN: $file (new file, $LINES lines > 400 soft limit)"
      fi
    fi
  done <<< "$CHANGED_SRC_FILES"
fi

if [ "$SIZE_FAIL" -gt 0 ]; then
  echo "FAIL — $SIZE_FAIL file(s) over hard limit:$SIZE_DETAILS"
elif [ "$SIZE_WARN" -gt 0 ]; then
  echo "WARN — $SIZE_WARN file(s) over soft limit:$SIZE_DETAILS"
else
  echo "PASS"
fi
```

FAIL if any changed file crosses 800. WARN if any crosses 400.

---

### CHECK 8: No Debug Artifacts

Scan the diff for debug statements and markers that should not ship.

```bash
DEBUG_HITS=""

DIFF=$(git diff "$BASE...$BRANCH" -- $CHANGED_SRC_FILES 2>/dev/null || true)

if [ -n "$DIFF" ]; then
  # Only look at added lines (starts with +, not ++)
  ADDED_LINES=$(echo "$DIFF" | grep '^+' | grep -v '^+++' || true)

  # Check for debug artifacts, excluding console.error in catch/error blocks
  ARTIFACTS=$(echo "$ADDED_LINES" | grep -nE '(console\.(log|debug|warn|info)|debugger;|// TODO|// FIXME|// HACK|// XXX)' || true)

  if [ -n "$ARTIFACTS" ]; then
    # Filter out console.error (allowed in error handlers)
    REAL_HITS=$(echo "$ARTIFACTS" | grep -v 'console\.error' || true)

    if [ -n "$REAL_HITS" ]; then
      DEBUG_HITS="$REAL_HITS"
    fi
  fi
fi

if [ -n "$DEBUG_HITS" ]; then
  echo "FAIL — debug artifacts found in diff:"
  echo "$DEBUG_HITS" | head -20
else
  echo "PASS"
fi
```

FAIL if any debug artifacts found in added lines (excluding test files and `console.error` in error handlers).

---

### CHECK 9: Pattern Quality

Heuristic warnings for code smells. These produce WARN, not FAIL.

```bash
PATTERN_WARNS=""

if [ -n "$CHANGED_SRC_FILES" ]; then
  while IFS= read -r file; do
    [ -z "$file" ] && continue
    [ ! -f "$file" ] && continue

    # 9a: If-chains — 3+ type-check branches in same function
    IF_CHAINS=$(grep -cE '(typeof|instanceof|===?\s*['\''"][a-z]+['\''"])' "$file" 2>/dev/null || echo 0)
    if [ "$IF_CHAINS" -ge 3 ]; then
      PATTERN_WARNS="${PATTERN_WARNS}\n  WARN 9a: $file has $IF_CHAINS type-check branches (consider polymorphism/map)"
    fi

    # 9b: Duplicated patterns — same non-trivial line appears 3+ times
    DUPES=$(grep -vE '^\s*(//|$|\{|\}|import|const|let|var|return|export)' "$file" 2>/dev/null | sort | uniq -c | sort -rn | awk '$1 >= 3 && length($0) > 30 {print}' | head -3 || true)
    if [ -n "$DUPES" ]; then
      PATTERN_WARNS="${PATTERN_WARNS}\n  WARN 9b: $file has duplicated patterns:\n$DUPES"
    fi

    # 9c: Event listener consistency — modal event types should match listeners
    MODAL_OPENS=$(grep -oE "openModal\(['\"][^'\"]+['\"]" "$file" 2>/dev/null | grep -oE "['\"][^'\"]+['\"]" | sort -u || true)
    MODAL_LISTENERS=$(grep -oE "onModalClose\(['\"][^'\"]+['\"]|modalType\s*===?\s*['\"][^'\"]+['\"]" "$file" 2>/dev/null | grep -oE "['\"][^'\"]+['\"]" | sort -u || true)
    if [ -n "$MODAL_OPENS" ] && [ -n "$MODAL_LISTENERS" ]; then
      UNMATCHED=$(comm -23 <(echo "$MODAL_OPENS") <(echo "$MODAL_LISTENERS") 2>/dev/null || true)
      if [ -n "$UNMATCHED" ]; then
        PATTERN_WARNS="${PATTERN_WARNS}\n  WARN 9c: $file opens modal types with no matching listener: $UNMATCHED"
      fi
    fi
  done <<< "$CHANGED_SRC_FILES"
fi

if [ -n "$PATTERN_WARNS" ]; then
  echo "WARN — pattern quality issues:$PATTERN_WARNS"
else
  echo "PASS"
fi
```

WARN only, never FAIL.

---

### CHECK 10: Uncommitted Files

Any untracked file that is imported by a committed file must also be committed.

```bash
UNCOMMITTED_FAILS=0
UNCOMMITTED_DETAILS=""

# Get untracked .js/.jsx/.sql/.md files
UNTRACKED=$(git ls-files --others --exclude-standard | grep -E '\.(js|jsx|sql|md)$' || true)

if [ -n "$UNTRACKED" ] && [ -n "$CHANGED_JS" ]; then
  while IFS= read -r untracked_file; do
    [ -z "$untracked_file" ] && continue
    BASENAME=$(basename "$untracked_file" | sed 's/\.\(js\|jsx\)$//')

    # Check if any committed changed file imports this untracked file
    IMPORTERS=$(echo "$CHANGED_JS" | xargs grep -l "$BASENAME" 2>/dev/null || true)

    if [ -n "$IMPORTERS" ]; then
      UNCOMMITTED_FAILS=$((UNCOMMITTED_FAILS + 1))
      UNCOMMITTED_DETAILS="${UNCOMMITTED_DETAILS}\n  $untracked_file (imported by: $IMPORTERS)"
    fi
  done <<< "$UNTRACKED"
fi

if [ "$UNCOMMITTED_FAILS" -gt 0 ]; then
  echo "FAIL — $UNCOMMITTED_FAILS uncommitted file(s) referenced by committed code:$UNCOMMITTED_DETAILS"
else
  echo "PASS"
fi
```

FAIL if any untracked file is imported by a committed file.

---

## Output Format

After running all 10 checks, produce the final report:

```
═══════════════════════════════════════════
           AGENT HARNESS RESULTS
═══════════════════════════════════════════
CHECK 1  Contract Exists ........... [PASS/FAIL]
CHECK 2  Tests Per Postcondition ... [PASS/FAIL]
CHECK 3  Tests Pass ................ [PASS/FAIL]
CHECK 4  Import Resolution ......... [PASS/FAIL]
CHECK 5  Data Shape Verification ... [PASS/FAIL]
CHECK 6  Build Passes .............. [PASS/FAIL/SKIP]
CHECK 7  File Size Limits .......... [PASS/FAIL/WARN]
CHECK 8  No Debug Artifacts ........ [PASS/FAIL]
CHECK 9  Pattern Quality ........... [PASS/WARN]
CHECK 10 Uncommitted Files ......... [PASS/FAIL]
───────────────────────────────────────────
VERDICT: [PASS / FAIL]
FAILURES: [list each FAIL with details]
WARNINGS: [list each WARN with details]
═══════════════════════════════════════════
```

---

## PERSIST HARNESS RESULTS (JSON)

After running all 10 checks, append results to the verification log JSON. This shares the same log file as enterprise-verify — all verification attempts (both verify and harness) appear in one audit trail.

```bash
node -e "
  const fs = require('fs');
  const f = '.claude/enterprise-state/<slug>-verification.json';
  let log = { verifications: [] };
  try { log = JSON.parse(fs.readFileSync(f)); } catch(e) {}
  log.verifications.push({
    type: 'harness',
    timestamp: new Date().toISOString(),
    checks: {
      contract_exists:       { result: '<PASS/FAIL>' },
      tests_per_pc:          { result: '<PASS/FAIL>', test_count: <N>, pc_count: <N> },
      tests_pass:            { result: '<PASS/FAIL>', new_failures: <N> },
      import_resolution:     { result: '<PASS/FAIL>', unresolved: <N> },
      data_shape:            { result: '<PASS/FAIL>', mismatches: <N> },
      build:                 { result: '<PASS/FAIL/SKIP>' },
      file_size:             { result: '<PASS/FAIL/WARN>' },
      debug_artifacts:       { result: '<PASS/FAIL>' },
      pattern_quality:       { result: '<PASS/WARN>' },
      uncommitted_files:     { result: '<PASS/FAIL>' }
    },
    overall: '<PASS/FAIL>'
  });
  fs.writeFileSync(f, JSON.stringify(log, null, 2));
  console.log('Harness results logged (' + log.verifications.length + ' total attempts)');
"
```

**Rules:**
- Same file as enterprise-verify — `.claude/enterprise-state/<slug>-verification.json`
- Always append, never overwrite
- Fill in actual values from the check results

---

## Decision Rules

| Outcome | Action |
|---------|--------|
| Any FAIL | Reject work. Send all failures back to builder with exact details. |
| WARN only | Pass with notes. Include warnings in merge commit message. |
| All PASS | Approve for merge. Proceed to cherry-pick or merge. |

### Re-run Policy

- Maximum 3 re-run iterations per task.
- After 3 failures, escalate to human with full harness output from all 3 runs.
- Each re-run must show improvement (fewer FAILs) or escalation triggers immediately.

---

## Usage

The orchestrator invokes this skill after receiving code from a builder:

1. Set `TASK_SLUG`, `BRANCH`, `BASE` variables.
2. Run all 10 checks in order.
3. Format the output report.
4. Apply decision rules.
5. If FAIL: send failure details back to builder, increment iteration counter.
6. If PASS: proceed to merge/cherry-pick.
