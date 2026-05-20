---
name: enterprise-review
description: "Two-stage code review: spec compliance THEN code quality. Separate concerns prevent spec bugs hiding behind quality observations. Medium+ tier requires a separate agent — builder never reviews own work. Use after enterprise-build."
---

# Enterprise Review

You are reviewing code that was built from a contract. Your job is adversarial verification — find what's wrong, not confirm what's right. Two stages, two separate concerns: spec compliance FIRST, code quality SECOND. They never mix.

---

## THE SEPARATION PRINCIPLE

```
Spec bugs hide behind quality observations.
"Clean code" that violates the contract is WORSE than messy code that fulfills it.
Review spec compliance FIRST. Only then review code quality.
```

Quality findings during Stage 1? Write them down, but DO NOT report them until Stage 2. Spec findings during Stage 2? STOP — you missed something. Go back to Stage 1.

---

## STACK RESOLUTION

Read `.claude/enterprise-state/stack-profile.json` at skill start. Extract:
- `$TEST_CMD` = `commands.test_all`
- `$SOURCE_DIR` = `structure.source_dirs.backend`
- `$FRONTEND_DIR` = `structure.source_dirs.frontend`
- `$TENANT_FIELD` = `multi_tenancy.field`
- `$TENANT_ENABLED` = `multi_tenancy.enabled`
- `$AUTH_MIDDLEWARE` = `auth.middleware_name`
- `$FILE_EXTENSIONS` = `conventions.file_extensions`

If no profile exists: BLOCKED — run /enterprise-discover first.

---

## PREREQUISITES

Before starting review:

1. **Verify upstream artifacts exist**:
   ```bash
   # Contract must exist
   ls docs/contracts/*contract* 2>/dev/null || echo "BLOCKED: No contract found"
   # Build must have produced changes
   git diff --stat HEAD 2>/dev/null | tail -1 || echo "BLOCKED: No changes to review"
   # Tests must be passing
   $TEST_CMD 2>&1 | tail -5
   ```
   **If any check fails: STOP.** Report what's missing.

2. **Identify the contract** — find the contract document in `docs/contracts/` or `.claude/designs/`
3. **Identify the plan** — find the plan in `docs/plans/`
4. **Identify all changed files** — run `git diff --name-only <base-branch>...HEAD`
5. **Identify the tier** — Micro/Small/Medium/Large/XL from the contract
6. **Check builder identity** — Medium+ tier: you MUST be a different agent than the builder

```
Medium+ Tier Gate:
- Ask: "Who built this?"
- If YOU built it → STOP. Tell the user a separate agent must review.
- Builder reviews own work = review is INVALID.
```

---

## SCOPE CLASSIFICATION

Before reviewing any code, classify EVERY changed file:

| Category | Definition | Review Action |
|----------|-----------|---------------|
| **REQUIRED** | Directly implements a postcondition | Full Stage 1 + Stage 2 |
| **ENABLING** | Infrastructure needed by REQUIRED files (utils, types, migrations) | Stage 2 only |
| **DRIFT** | Not traceable to any postcondition | Flag for removal |

```bash
# List all changed files
git diff --name-only <base-branch>...HEAD

# For each file, answer: which postcondition does this serve?
# If no postcondition → DRIFT
```

**DRIFT files are a red flag.** They indicate scope creep. Report them prominently. The builder must justify each one or revert it.

---

## STAGE 1: SPEC COMPLIANCE

### 1A — Postcondition Verification

For EACH postcondition in the contract (PC-1, PC-2, etc.):

```
PC-X: [postcondition text]
├── Implemented? YES/NO
│   └── Where? [file:line]
├── Test exists? YES/NO
│   └── Where? [test file:line]
├── Test verifies the RIGHT thing? YES/NO
│   └── Does the assertion match the postcondition exactly?
│   └── Does the test exercise the actual code path (not a mock)?
│   └── Does the test fail if the postcondition is violated?
└── Verdict: PASS / FAIL [reason]
```

**Common spec failures:**
- Test passes but doesn't actually verify the postcondition (assertion too weak)
- Implementation handles happy path but not the error case stated in the PC
- Test mocks the exact thing the postcondition is about
- Postcondition says "returns X" but implementation returns X wrapped in something else

### 1B — Consumer Map Verification

For each consumer listed in the contract's consumer map:

```
Consumer: [consumer name]
├── Still receives correct data shape? YES/NO
├── Breaking changes introduced? YES/NO
├── Integration tested? YES/NO
└── Verdict: PASS / FAIL [reason]
```

```bash
# Find all consumers of the changed module
cd $PROJECT_ROOT
grep -rn "require.*<module>" $SOURCE_DIR/ --include="*.js" | grep -v node_modules | grep -v __tests__
grep -rn "import.*from.*<module>" $SOURCE_DIR/ --include="*.js" | grep -v node_modules | grep -v __tests__
```

### 1C — Invariant Verification

For each invariant in the contract:

```
Invariant: [invariant text]
├── Maintained in all code paths? YES/NO
├── Test guards the invariant? YES/NO
└── Verdict: PASS / FAIL [reason]
```

### 1D — Stage 1 Verdict

```
═══════════════════════════════════════════
STAGE 1 VERDICT: SPEC [PASS/FAIL]
═══════════════════════════════════════════

Postconditions: X/Y passed
Consumers: X/Y verified
Invariants: X/Y maintained

[If FAIL:]
FAILURES:
- PC-X: [specific failure]
- Consumer Y: [specific failure]
- Invariant Z: [specific failure]

ACTION: Fix failures and re-submit for review.
Stage 2 will NOT run until Stage 1 passes.
═══════════════════════════════════════════
```

**If Stage 1 FAILS: STOP. Do not proceed to Stage 2.** Report failures and return to builder.

---

## STAGE 2: CODE QUALITY

Only runs after Stage 1 passes. Stage 2 has 8 quality lenses.

### 2A — File Size

```bash
# Check all changed files for line count
cd $PROJECT_ROOT
for f in $(git diff --name-only <base-branch>...HEAD | grep -E "$FILE_EXTENSIONS"); do
  lines=$(wc -l < "$f" 2>/dev/null || echo "MISSING")
  if [ "$lines" != "MISSING" ] && [ "$lines" -gt 400 ]; then
    echo "OVER 400: $f ($lines lines)"
  fi
done
```

- Soft limit: 400 lines. Flag files over 400.
- Hard limit: 800 lines. FAIL files over 800 (unless pre-existing legacy).
- Test files are exempt from line limits.

### 2B — Tenant Isolation

```bash
# Find all new SQL queries in changed files
cd $PROJECT_ROOT
for f in $(git diff --name-only <base-branch>...HEAD | grep -E "$FILE_EXTENSIONS"); do
  # Show new lines with SQL keywords
  git diff <base-branch>...HEAD -- "$f" | grep "^+" | grep -iE "(SELECT|INSERT|UPDATE|DELETE|FROM)" | head -20
done
```

For EACH new query:
- Has `$TENANT_FIELD` in WHERE clause? (Exception: `customers` table has no `$TENANT_FIELD`)
- Has `$TENANT_FIELD` in INSERT values?
- Uses parameterized query (no string interpolation)?

### 2C — Query Safety

```bash
# Find potential SQL injection vectors in changed files
cd $PROJECT_ROOT
for f in $(git diff --name-only <base-branch>...HEAD | grep -E "$FILE_EXTENSIONS"); do
  git diff <base-branch>...HEAD -- "$f" | grep "^+" | grep -E '(\$\{|` ?\+|string concat)' | grep -iE "(SELECT|INSERT|UPDATE|DELETE)" | head -10
done
```

- ALL queries must use parameterized placeholders (`$1`, `$2`, etc.)
- No string concatenation in SQL
- No template literals building SQL with user input

### 2D — Import Verification

```bash
# Verify every import in changed files resolves
cd $PROJECT_ROOT
for f in $(git diff --name-only <base-branch>...HEAD | grep -E "$FILE_EXTENSIONS"); do
  echo "=== $f ==="
  grep -n "require(" "$f" | while read -r line; do
    # Extract the module path
    mod=$(echo "$line" | grep -oP "require\(['\"]([^'\"]+)" | sed "s/require(['\"]//")
    if [[ "$mod" == .* ]]; then
      # Relative import — check file exists
      dir=$(dirname "$f")
      resolved="$dir/$mod"
      if [ ! -f "$resolved" ] && [ ! -f "${resolved}.js" ] && [ ! -f "${resolved}/index.js" ]; then
        echo "  MISSING: $mod (from line: $line)"
      fi
    fi
  done
done
```

### 2E — Debug Code

```bash
# Find debug artifacts in changed files (excluding test files)
cd $PROJECT_ROOT
for f in $(git diff --name-only <base-branch>...HEAD | grep -E "$FILE_EXTENSIONS" | grep -v __tests__ | grep -v '\.test\.' | grep -v '\.spec\.'); do
  git diff <base-branch>...HEAD -- "$f" | grep "^+" | grep -nE "(console\.(log|debug|warn)|debugger|TODO|FIXME|HACK|XXX)" | head -10
  if [ $? -eq 0 ]; then
    echo "  ^^^ in $f"
  fi
done
```

- `console.log` / `console.debug` in production code = FAIL
- `console.warn` / `console.error` with context = OK (they're intentional logging)
- `debugger` statements = FAIL
- `TODO` / `FIXME` / `HACK` / `XXX` = FLAG (not auto-fail, but must be intentional)

### 2F — Security

For each new route or endpoint:
- Auth middleware applied? (`$AUTH_MIDDLEWARE` or equivalent)
- Permission checks present? (role-based access)
- Input validation present? (request body/params validated)
- Route order correct? (public routes before auth middleware)

```bash
# Find new route definitions
cd $PROJECT_ROOT
for f in $(git diff --name-only <base-branch>...HEAD | grep -E "$FILE_EXTENSIONS"); do
  git diff <base-branch>...HEAD -- "$f" | grep "^+" | grep -E "router\.(get|post|put|patch|delete)" | head -10
  if [ $? -eq 0 ]; then
    echo "  ^^^ in $f"
  fi
done
```

### 2G — Pattern Compliance

- Does the code follow existing patterns in the codebase?
- Are there unnecessary abstractions not seen elsewhere?
- Does error handling match existing conventions?
- Are existing utilities reused (not reinvented)?

```bash
# Check if similar patterns exist in codebase
cd $PROJECT_ROOT
# Example: if new code creates a service, check existing service patterns
ls $SOURCE_DIR/services/*.js | head -5
# Compare structure with existing services
```

### 2H — Migration Safety (if applicable)

```bash
# Check migration files in the diff
cd $PROJECT_ROOT
git diff --name-only <base-branch>...HEAD | grep -E 'migrations/.*\.sql$'
```

For each migration:
- Uses `IF NOT EXISTS` / `IF EXISTS` guards?
- Uses `TIMESTAMPTZ` (not `TIMESTAMP`)?
- Adds indexes for foreign keys?
- Reversible? (or documented as irreversible)

### 2I — Stage 2 Verdict

```
═══════════════════════════════════════════
STAGE 2 VERDICT: QUALITY [PASS/FAIL]
═══════════════════════════════════════════

File Size:        PASS/FAIL [details]
Tenant Isolation: PASS/FAIL [details]
Query Safety:     PASS/FAIL [details]
Import Resolution:PASS/FAIL [details]
Debug Code:       PASS/FAIL [details]
Security:         PASS/FAIL [details]
Pattern Compliance: PASS/FAIL [details]
Migration Safety: PASS/FAIL [details if applicable]

[If FAIL:]
FAILURES:
- 2X: [specific failure and fix required]

ACTION: Fix failures and re-submit for review.
═══════════════════════════════════════════
```

---

## FINAL REVIEW REPORT

Save to: `docs/reviews/YYYY-MM-DD-<slug>-review.md`

```markdown
# Review: <Feature Slug>

**Date:** YYYY-MM-DD
**Contract:** <path to contract>
**Builder:** <who built it>
**Reviewer:** <who reviewed it>
**Tier:** <Micro/Small/Medium/Large/XL>

## Scope Classification

| File | Category | Postcondition |
|------|----------|---------------|
| ... | REQUIRED | PC-X |
| ... | ENABLING | supports PC-Y |
| ... | DRIFT | none — flagged |

## Stage 1: Spec Compliance — [PASS/FAIL]

### Postconditions
| PC | Status | Implementation | Test | Notes |
|----|--------|---------------|------|-------|
| PC-1 | PASS/FAIL | file:line | test:line | ... |

### Consumers
| Consumer | Status | Notes |
|----------|--------|-------|
| ... | PASS/FAIL | ... |

### Invariants
| Invariant | Status | Notes |
|-----------|--------|-------|
| ... | PASS/FAIL | ... |

## Stage 2: Code Quality — [PASS/FAIL]

| Check | Status | Notes |
|-------|--------|-------|
| File Size | PASS/FAIL | ... |
| Tenant Isolation | PASS/FAIL | ... |
| Query Safety | PASS/FAIL | ... |
| Import Resolution | PASS/FAIL | ... |
| Debug Code | PASS/FAIL | ... |
| Security | PASS/FAIL | ... |
| Pattern Compliance | PASS/FAIL | ... |
| Migration Safety | PASS/FAIL | ... |

## Overall Verdict: [PASS/FAIL]

[Summary of findings, required fixes, or approval statement]
```

---

## REVIEW WORKFLOW

```
1. Receive review request
2. Locate contract + plan + changed files
3. Check tier → enforce builder != reviewer for Medium+
4. Classify scope: REQUIRED / ENABLING / DRIFT
5. Stage 1: Spec Compliance
   └── FAIL? → STOP. Return to builder with failures.
6. Stage 2: Code Quality
   └── FAIL? → Return to builder with failures.
7. Both PASS → Write review report → Approve
```

---

## RE-REVIEW PROTOCOL

When code comes back after fixes:

1. **Only re-check the failures** — don't re-review passing checks
2. **Verify the fix didn't break a previously passing check** — run all tests
3. **Update the review report** with new verdicts
4. **If new issues found during re-review** — full stage re-run for that stage

```bash
# Verify tests still pass after fixes
cd $PROJECT_ROOT && $TEST_CMD 2>&1 | tail -20
```
