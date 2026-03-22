---
name: coco-fix-iterate
description: Iterative quality convergence loop with multi-agent architecture. Reviews, scores, fixes, and re-scores code until target quality is reached. Use /coco-fix-iterate [--score N] [--max-iterations N] [--single-agent] [focus].
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task
---

# COCO Fix Iterate

Autonomous iterative quality loop that reviews, scores, plans fixes, applies them, verifies, and re-scores — repeating until the code reaches a target quality score.

Uses a **multi-agent architecture by default**: separate subagents for reviewing, fixing, and verifying. This prevents self-bias (an agent reviewing its own code tends to be lenient) and produces more objective results.

## How it works

This skill is **agent-implemented** — the agent reads the steps below and executes them autonomously. There is no standalone bash script.

```
/coco-fix-iterate
/coco-fix-iterate --score 90
/coco-fix-iterate --max-iterations 5 security
/coco-fix-iterate --single-agent                # disable multi-agent, use one agent for everything
```

## Input

- `$ARGUMENTS` may contain:
  - `--score N` — Target score threshold (default: 85)
  - `--max-iterations N` — Maximum iteration cycles (default: 10)
  - `--single-agent` — Disable multi-agent mode; one agent does everything (faster but less objective)
  - Remaining text = focus area (e.g., "security", "tests", "src/api/")

### Examples

```
/coco-fix-iterate                              # Full project, score >= 85, multi-agent
/coco-fix-iterate --score 90                   # Higher quality bar
/coco-fix-iterate --max-iterations 5 security  # Focus on security, max 5 rounds
/coco-fix-iterate --single-agent               # One agent does everything (faster)
/coco-fix-iterate src/api/                     # Focus on specific directory
```

## Parse Arguments

```bash
# Default values
TARGET_SCORE=85
MAX_ITERATIONS=10
MULTI_AGENT=true          # Multi-agent ON by default
FOCUS=""

# Parse from $ARGUMENTS
# --score N -> TARGET_SCORE=N
# --max-iterations N -> MAX_ITERATIONS=N
# --single-agent -> MULTI_AGENT=false
# remaining text -> FOCUS
```

## Multi-Agent Architecture

By default, each iteration uses **3 specialized subagents** via the `Task` tool, each with a distinct role and restricted scope. This separation forces objectivity: the reviewer never sees the fixer's reasoning, and the verifier has no bias toward the fixes.

```
┌─────────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (this agent)                                      │
│  Controls the loop, tracks scores, checks convergence           │
│                                                                 │
│  For each iteration:                                            │
│                                                                 │
│    ┌──────────────────┐                                         │
│    │  REVIEWER AGENT   │  Task(subagent_type="general-purpose") │
│    │  Read-only        │  - Reads code, runs checks             │
│    │  No editing       │  - Scores 12 dimensions                │
│    │                   │  - Classifies issues P0-P3             │
│    │  Returns: score,  │  - Returns structured report           │
│    │  issues, plan     │  - Has NO context of previous fixes    │
│    └────────┬─────────┘                                         │
│             │                                                   │
│             ▼                                                   │
│    ┌──────────────────┐                                         │
│    │  FIXER AGENT      │  Task(subagent_type="general-purpose") │
│    │  Can edit files   │  - Receives ONLY the issue list        │
│    │  No reviewing     │  - Applies fixes P0 → P1 → P2         │
│    │                   │  - Max 5-7 fixes per iteration         │
│    │  Returns: list    │  - Returns list of changes made        │
│    │  of changes       │  - Has NO access to scores             │
│    └────────┬─────────┘                                         │
│             │                                                   │
│             ▼                                                   │
│    ┌──────────────────┐                                         │
│    │  VERIFIER AGENT   │  Task(subagent_type="general-purpose") │
│    │  Read-only        │  - Runs full test suite                │
│    │  No editing       │  - Checks nothing is broken            │
│    │                   │  - Reports pass/fail per check         │
│    │  Returns: test    │  - Has NO context of what was fixed    │
│    │  results          │  - Objective "does it work?" answer    │
│    └──────────────────┘                                         │
│                                                                 │
│  Orchestrator evaluates results → convergence check → next iter │
└─────────────────────────────────────────────────────────────────┘
```

### Why multi-agent is better

| Aspect | Single agent | Multi-agent (default) |
|---|---|---|
| **Review objectivity** | Tends to be lenient with own code | Fresh eyes, no self-bias |
| **Fix quality** | May over-engineer based on review context | Focused only on the issue list |
| **Verification** | May skip tests it "knows" pass | Runs everything blindly |
| **Token efficiency** | One large context | Smaller focused contexts |
| **Speed** | Faster (no subagent overhead) | Slightly slower per iteration |

### When to use `--single-agent`

- Quick fixes on small codebases
- When token budget is limited
- When you need speed over objectivity
- Prototypes or spikes

## Algorithm

```
ITERATION = 0
PREVIOUS_SCORE = 0
SCORE_HISTORY = []
CONSECUTIVE_AT_TARGET = 0      # counted only after successful verify; must reach 2 to converge
COVERAGE_HISTORY = []          # coverage % per iteration (None if not available)
PENDING_COVERAGE_DEBT = False  # True when coverage dropped; next Fixer must add tests first
PREV_ISSUES = set()            # issue keys from the PREVIOUS iteration (for recurring detection)

# Issue key format: "<file>:<first-6-words-of-description-lowercased-slugified>"
# Example: "src/auth/flow.ts:missing_error_handling_in_token_refresh"
# Using file + description words (not line number) makes keys stable across fixes that shift lines.
SEEN_ISSUES = {}               # {issue_key: first_iteration_seen}

while ITERATION < MAX_ITERATIONS:
    ITERATION += 1

    # 1. REVIEW (Reviewer Agent or self)
    score, issues = review(FOCUS)
    SCORE_HISTORY.append(score)

    # 1b. IDENTIFY RECURRING ISSUES and UPDATE TRACKING
    current_keys = {make_key(i) for i in issues}   # "<file>:<first-6-words-slugified>"
    recurring_keys = current_keys & PREV_ISSUES     # present in BOTH this AND previous iteration
    PREV_ISSUES = current_keys                      # update for next iteration
    for key in current_keys:
        if key not in SEEN_ISSUES:
            SEEN_ISSUES[key] = ITERATION

    # 2. CHECK EARLY EXITS (before fixing — no point fixing if we should stop)
    if score >= 95:
        EXCELLENT → STOP  # exceptionally high quality; no need for 2-iteration stability
    if ITERATION >= 5 and score < TARGET_SCORE - 20 and no_improvement(SCORE_HISTORY, 3):
        STUCK → STOP  # below minimum threshold with no progress; needs manual intervention
    if len(recurring_keys) >= 3 and no_improvement(SCORE_HISTORY, 3):
        STUCK → STOP  # same issues unfixed across multiple iterations with no progress
    if is_oscillating(SCORE_HISTORY):
        OSCILLATING → STOP
    if is_diminishing(SCORE_HISTORY):
        DIMINISHING → STOP
    if ITERATION >= 3 and is_stalled(SCORE_HISTORY):
        STALLED → STOP  # last 2 deltas both < 2 pts; at noise floor, stop wasting iterations

    # 3. PLAN FIXES (Orchestrator — P0 first, then P1, then P2)
    plan = prioritize(issues, recurring_keys)

    # 4. APPLY FIXES (Fixer Agent or self)
    changes, files_modified = fix(plan, pending_coverage_debt=PENDING_COVERAGE_DEBT)

    # 5. VERIFY (Verifier Agent or self)
    verify_result, coverage = verify()
    if not verify_result:
        # Ask a new Fixer task to undo files_modified from this iteration
        # Re-verify; if still failing: log failure, keep pre-fix state, continue
        LOG verify_failure; SKIP score/counter update; continue

    # 6. UPDATE CONVERGENCE COUNTER (only after successful verify)
    if score >= TARGET_SCORE:
        CONSECUTIVE_AT_TARGET += 1
    else:
        CONSECUTIVE_AT_TARGET = 0

    if CONSECUTIVE_AT_TARGET >= 2 and |score - PREVIOUS_SCORE| < 5:
        CONVERGED → STOP  # 2 consecutive successful iterations at target, stable within 5 points

    # 7. UPDATE COVERAGE TRACKING
    if coverage != None:
        COVERAGE_HISTORY.append(coverage)
        if len(COVERAGE_HISTORY) >= 2 and coverage < COVERAGE_HISTORY[-2] - 1:
            PENDING_COVERAGE_DEBT = True   # next Fixer must add tests before new fixes
        else:
            PENDING_COVERAGE_DEBT = False
    # If coverage is N/A, PENDING_COVERAGE_DEBT is unchanged from previous iteration

    PREVIOUS_SCORE = score

# Loop exhausted without convergence
MAX_ITERATIONS → STOP

REPORT final results

# Helper function definitions:
# no_improvement(history, n): True if the last n scores are all equal or decreasing
#   example: no_improvement([60, 62, 62, 62], 3) → True (no gain in last 3)
# is_oscillating(history): True if the last 4 scores alternate up/down with total swing < 3 points
#   example: is_oscillating([70, 73, 71, 74]) → True
# is_diminishing(history): True if the last 3 score improvements are all < 1 point
#   example: is_diminishing([80, 80.5, 81, 81.3]) → True
# is_stalled(history): True if len(history) >= 3 AND both last 2 deltas are < 2 points (abs value or regression)
#   example: is_stalled([72, 74, 75, 76]) → True  (deltas: +1, +1 — both < 2)
#   example: is_stalled([72, 74, 78, 79]) → False (deltas: +4, +1 — only last 1 is < 2)
#   example: is_stalled([80, 89, 76, 77]) → True  (deltas: -13, +1 — both < 2 in abs value: |-13|... wait)
#   Note: "< 2" applies to the IMPROVEMENT (positive delta only). A regression (negative delta) always counts as < 2.
#   So: delta < 2 means (score[i] - score[i-1]) < 2  i.e. improved by less than 2 points, or went down
# make_key(issue): returns "<file>:<first-6-words-of-description-lowercased-slugified>"
#   example: make_key({file:"src/foo.ts", desc:"Missing error handling in token refresh path"})
#            → "src/foo.ts:missing_error_handling_in_token_refresh"
```

## Phase 1: Review (REVIEWER AGENT)

The orchestrator launches a **Reviewer Agent** via the `Task` tool.

**CRITICAL RULE FOR ORCHESTRATOR**: The reviewer prompt must NEVER contain any reference to
previous iterations, previous scores, what was fixed, or what changed. Copy the template below
verbatim — only substitute PROJECT_DIR, FOCUS, and the detected check commands.

```
Task(
  subagent_type = "general-purpose",
  prompt = """
  You are a STRICT EXTERNAL CODE AUDITOR. You have NEVER seen this codebase before.
  You have NO knowledge of any previous reviews, fixes, or improvements to this code.
  You are READ-ONLY — do NOT modify any files.

  Review the code as if you are an external auditor hired to certify quality.
  Be strict. Do NOT give benefit of the doubt. Score what exists, not what was intended.
  A passing test is the baseline expectation, not a virtue.

  PROJECT: {PROJECT_DIR}
  FOCUS: {FOCUS or "entire codebase — read all source files"}

  ── STEP 1: Run automated checks ──────────────────────────────────────────────

  Run EACH of these commands and capture full output:

  [If pnpm-lock.yaml exists]:
    pnpm format 2>&1 || true
    pnpm typecheck 2>&1 || true
    pnpm lint 2>&1 || true
    pnpm test 2>&1 || true

  [If yarn.lock exists]:
    yarn typecheck 2>&1 || true
    yarn lint 2>&1 || true
    yarn test 2>&1 || true

  [If package-lock.json exists]:
    npm run typecheck 2>&1 || true
    npm run lint 2>&1 || true
    npm test 2>&1 || true

  [If Cargo.toml exists]:
    cargo clippy 2>&1 || true
    cargo test 2>&1 || true

  [If pyproject.toml exists]:
    ruff check . 2>&1 || true
    pytest 2>&1 || true

  [If build.gradle or build.gradle.kts exists]:
    ./gradlew check 2>&1 || true

  Record every error, warning, and failure. A lint warning counts as an issue.

  ── STEP 2: Read and analyze source code ──────────────────────────────────────

  Read the actual source files. Do not assume anything works until you verify it.
  Check each of the 12 dimensions below. For each, look for real evidence, not absence of evidence.

  ── STEP 3: Score each dimension 0-100 and calculate weighted total ───────────

  | Dimension       | Weight | What to check |
  |-----------------|--------|---------------|
  | Correctness     | 15%    | Logic errors, wrong outputs, failing tests, edge cases not handled |
  | Completeness    | 10%    | Missing features, stubs, TODOs, unimplemented paths |
  | Robustness      | 10%    | Missing error handling, uncaught exceptions, no input validation |
  | Readability     | 10%    | Confusing names, long functions, unclear intent |
  | Maintainability | 10%    | Hard to change, tight coupling, poor separation of concerns |
  | Complexity      | 8%     | Unnecessary complexity, over-engineering, hard-to-follow flow |
  | Duplication     | 7%     | Copy-pasted code, repeated logic that should be abstracted |
  | Test Coverage   | 10%    | Untested paths, missing edge case tests, no integration tests |
  | Test Quality    | 5%     | Tests that don't assert anything meaningful, trivial tests |
  | Security        | 8%     | Injection vulnerabilities, exposed secrets, unsafe operations |
  | Documentation   | 4%     | Missing JSDoc/docstrings on public APIs, unclear contracts |
  | Style           | 3%     | Formatting violations, naming inconsistencies, lint errors |

  Weighted total = sum(dimension_score * weight)

  ── SCORING CALIBRATION ───────────────────────────────────────────────────────

  95-100: Virtually no issues. Production-ready, exemplary code.
  85-94:  Good code with only minor, non-blocking issues. Ready for review.
  70-84:  Several issues. Works but needs improvement before production.
  50-69:  Significant problems. Multiple failing areas.
  Below 50: Major deficiencies. Core functionality broken or insecure.

  When in doubt, score lower. A score of 85 should be genuinely hard to achieve.

  ── STEP 4: Classify every issue ──────────────────────────────────────────────

  P0 Critical:  Breaks functionality, security vulnerability, data loss risk
  P1 High:      Significant quality problem, missing error handling, test failures
  P2 Medium:    Code quality issue, maintainability concern, missing coverage
  P3 Low:       Cosmetic, style, minor inconsistency

  ── RETURN FORMAT (use EXACTLY this structure) ────────────────────────────────

  ---SCORE: XX
  ---ISSUES:
  - P0: [file:line] description
  - P1: [file:line] description
  - P2: [file:line] description
  ---DIMENSIONS:
  Correctness: XX
  Completeness: XX
  Robustness: XX
  Readability: XX
  Maintainability: XX
  Complexity: XX
  Duplication: XX
  Test Coverage: XX
  Test Quality: XX
  Security: XX
  Documentation: XX
  Style: XX
  ---AUTOMATED_CHECKS:
  typecheck: PASS/FAIL (N errors)
  lint: PASS/FAIL (N warnings/errors)
  tests: PASS/FAIL (N passed, N failed)
  """
)
```

If `--single-agent` is set, the orchestrator performs this review itself instead of launching a subagent.
When reviewing as self, apply the same strict calibration — do not be lenient because you wrote the fixes.

### 1.1 Automated Checks (single-agent mode reference)

When `--single-agent` is set, the orchestrator runs these commands directly (same commands as embedded in the Reviewer Agent prompt above — listed here for single-agent convenience):

```bash
# Auto-detect project type and run checks
if [ -f "pnpm-lock.yaml" ]; then
  pnpm format 2>&1 || true
  pnpm typecheck 2>&1 || true
  pnpm lint 2>&1 || true
  pnpm test 2>&1 || true
elif [ -f "yarn.lock" ]; then
  yarn typecheck 2>&1 || true
  yarn lint 2>&1 || true
  yarn test 2>&1 || true
elif [ -f "package-lock.json" ]; then
  npm run typecheck 2>&1 || true
  npm run lint 2>&1 || true
  npm test 2>&1 || true
elif [ -f "Cargo.toml" ]; then
  cargo clippy 2>&1 || true
  cargo test 2>&1 || true
elif [ -f "pyproject.toml" ]; then
  ruff check . 2>&1 || true
  pytest 2>&1 || true
elif [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
  ./gradlew check 2>&1 || true
fi
```

### 1.2 Manual Code Analysis

Read and analyze code across the 12 dimensions:

| Dimension | Weight |
|---|---|
| Correctness | 15% |
| Completeness | 10% |
| Robustness | 10% |
| Readability | 10% |
| Maintainability | 10% |
| Complexity | 8% |
| Duplication | 7% |
| Test Coverage | 10% |
| Test Quality | 5% |
| Security | 8% |
| Documentation | 4% |
| Style | 3% |

### 1.3 Score and Classify

Calculate weighted score. Classify all issues by severity (P0/P1/P2/P3).

### 1.4 Display Iteration Header

The orchestrator displays:

```
╔══════════════════════════════════════╗
║  ITERATION 1 / 10        [3 agents] ║
║  Score: XX/100 (Grade X)            ║
║  Target: 85  |  Issues: N           ║
║  P0: N  P1: N  P2: N  P3: N        ║
╚══════════════════════════════════════╝
```

## Phase 2: Convergence Check (ORCHESTRATOR)

The orchestrator (not a subagent) checks if we should stop:

### 2.1 Target Reached
```
IF CONSECUTIVE_AT_TARGET >= 2 AND |score - PREVIOUS_SCORE| < 5:
  → STOP (converged — 2 consecutive successful iterations at target, stable within 5 points)
```
Note: `CONSECUTIVE_AT_TARGET` increments when `score >= TARGET_SCORE` **and verify passes**, resets to 0 when `score < TARGET_SCORE`. When verify fails, the `continue` skips the counter update entirely — the counter is **preserved** from the previous successful iteration (since the review score is still valid for the pre-fix codebase).

### 2.2 Excellent Quality
```
IF score >= 95:
  → STOP (EXCELLENT — score is exceptionally high)
```
Note: This fires before fix/verify. It is valid because the Reviewer already ran all automated checks (tests, typecheck, lint) in Step 1 — a 95+ score implies they passed.

### 2.3 Oscillating
```
IF last 4 scores alternate up/down with delta < 3:
  → STOP (OSCILLATING — no further progress possible)
```

### 2.4 Diminishing Returns
```
IF last 3 improvements are all < 1 point:
  → STOP (DIMINISHING)
```

### 2.4b Stalled
```
IF iteration >= 3 AND last 2 deltas are both < 2 points (including regressions):
  → STOP (STALLED — AI cannot improve further; remaining issues are design decisions or noise)
```
Note: This catches the case where the model has run out of clear fixes. Fresh reviewers scoring the same code within ±2 points of each other indicates we are at the noise floor. Continuing wastes iterations without meaningful quality gains.

### 2.5 Stuck

Two independent conditions trigger STUCK:

**(a) Below minimum threshold:**
```
IF iteration >= 5 AND score < TARGET_SCORE - 20 AND no_improvement(SCORE_HISTORY, 3):
  → STOP (STUCK — below minimum threshold with no progress; needs manual intervention)
```

**(b) Recurring unfixed issues with no progress:**
```
IF len(recurring_keys) >= 3 AND no_improvement(SCORE_HISTORY, 3):
  → STOP (STUCK — same issues unfixed across multiple iterations with no progress)
```

Both are checked in the early-exit block of the algorithm (before Phase 3 — before any fixing).

### 2.6 Max Iterations

The `while ITERATION < MAX_ITERATIONS` loop guard prevents running a 11th iteration when `MAX_ITERATIONS=10`. The last allowed iteration (ITERATION = MAX_ITERATIONS) runs all phases (review, fix, verify) before the loop exits.

After the loop exits:
```
MAX_ITERATIONS → STOP  (all iterations used; no convergence reached)
```

Note: this stop fires after the last complete iteration, NOT mid-iteration. An agent following Section 2 phases does not need to add a redundant check here — the loop guard handles it.

## Phase 3: Plan Fixes (ORCHESTRATOR)

The orchestrator creates the fix plan from the reviewer's output. This stays in the orchestrator to maintain control:

0. **Check for recurring issues** — recurring issues are those whose key appears in BOTH the current iteration AND the previous iteration's `PREV_ISSUES` set (computed in Step 1b of the algorithm):
   - If an issue key appears in `recurring_keys`, mark it `RECURRING`. This means the previous fix attempt did not work.
   - For RECURRING P0/P1 issues: do NOT re-attempt the same fix strategy — escalate in the fixer
     prompt: "Previous attempt to fix this failed. Try a fundamentally different approach."
   - If `len(recurring_keys) >= 3 AND no_improvement(SCORE_HISTORY, 3)`, the pseudocode will stop with `STUCK` before reaching this phase.

1. **Select issues to fix this iteration** — prioritize:
   - All P0 (Critical) issues — always fix these
   - P1 (High) issues — fix as many as feasible
   - P2 (Medium) — fix only if P0 and P1 are clear
   - Never fix P3 in the loop (cosmetic, not worth the churn risk)

2. **Estimate impact** — focus on fixes that will improve the score the most:
   - Fixing a failing test (Correctness +15%)
   - Adding missing error handling (Robustness +10%)
   - Adding tests for uncovered code (Test Coverage +10%)

3. **Limit scope per iteration** — max 5-7 fixes per cycle to keep changes reviewable

## Phase 4: Apply Fixes (FIXER AGENT)

The orchestrator launches a **Fixer Agent** via the `Task` tool:

```
Task(
  subagent_type = "general-purpose",
  prompt = """
  You are a CODE FIXER. Your job is to apply specific fixes to this codebase.
  You receive a list of issues — fix them one by one.

  [If PENDING_COVERAGE_DEBT is True, include this block — otherwise omit it]:
  COVERAGE DEBT (resolve before any new logic fixes):
  Coverage dropped in the last iteration. Before applying the fixes below, write tests
  for any untested logic added in the previous iteration. Once coverage is restored,
  proceed with the fixes below.

  FIXES TO APPLY:
  1. P0: [file:line] description
  2. P1: [file:line] description
  ...

  RULES:
  - Fix ONLY the listed issues, nothing else
  - Minimal changes — fix the issue, not the neighborhood
  - Run `pnpm format:fix` before committing — formatting errors fail CI
  - Run typecheck after each fix to catch regressions
  - Apply fixes in priority order: all P0s first, then P1s, then P2s
  - If a fix breaks something: first try to resolve it (including writing the test below);
    if still broken after 2 attempts, revert the fix entirely and mark it SKIPPED
  - Max 5-7 fixes per session
  - Do NOT commit anything

  TEST REQUIREMENT (applies to every P0 and P1 fix that changes logic, not just structure):
  - After applying each logic fix, write a regression test that:
      (a) directly targets the bug scenario described in the issue (demonstrates the bug was real, not incidental coverage)
      (b) PASSES on the fixed code
  - Place the test in the appropriate colocated test file (*.test.ts, *_test.go, test_*.py, etc.)
  - Run the test immediately after writing to confirm it passes — if it does not, make ONE
    revision attempt; if still failing after that, revert the fix entirely per RULES above
  - Structural-only fixes (rename, move, reorder) do NOT require a new test
  - Do NOT write tests for issues you SKIPPED

  After all fixes, return this EXACT format:
  ---CHANGES:
  - FIXED: [file:line] description (what you changed)
  - SKIPPED: [file:line] description (why you skipped it)
  ---TESTS_WRITTEN:
  - [test_file:line] test name — covers fix for [original_file:line]
  - NONE (if no logic fixes were applied)
  ---FILES_MODIFIED:
  - path/to/file1.ts
  - path/to/test1.test.ts
  """
)
```

If `--single-agent` is set, the orchestrator applies fixes itself.

### Fix Safety Rules

- **Never change more than needed** — fix the issue, not the neighborhood
- **If tests fail after a fix, revert** — a fix that breaks tests is not a fix
- **Track what was changed** — maintain a list of modified files and changes
- **Preserve git history** — do NOT commit during the loop (user decides when to commit)

## Phase 5: Verify (VERIFIER AGENT)

The orchestrator launches a **Verifier Agent** via the `Task` tool:

```
Task(
  subagent_type = "general-purpose",
  prompt = """
  You are a CODE VERIFIER. Your job is to check if this codebase works correctly.
  You are READ-ONLY — do NOT modify any files.

  PROJECT: {PROJECT_DIR}

  Run each of the following commands and capture full output:

  [If pnpm-lock.yaml exists]:
    pnpm format 2>&1 || true
    pnpm typecheck 2>&1 || true
    pnpm lint 2>&1 || true
    pnpm test 2>&1 || true
    # Run coverage separately; skip silently if not configured:
    pnpm test --coverage 2>&1 || true

  [If yarn.lock exists]:
    yarn typecheck 2>&1 || true
    yarn lint 2>&1 || true
    yarn test 2>&1 || true
    yarn test --coverage 2>&1 || true

  [If package-lock.json exists]:
    npm run typecheck 2>&1 || true
    npm run lint 2>&1 || true
    npm test 2>&1 || true
    npm test -- --coverage 2>&1 || true

  [If Cargo.toml exists]:
    cargo clippy 2>&1 || true
    cargo test 2>&1 || true

  [If pyproject.toml exists]:
    ruff check . 2>&1 || true
    pytest --cov 2>&1 || true

  [If build.gradle or build.gradle.kts exists]:
    ./gradlew check 2>&1 || true
    ./gradlew jacocoTestReport 2>&1 || true

  For coverage: extract the overall line/statement coverage % from the output.
  If coverage is not configured or the command fails, report N/A.

  Return this EXACT format:
  ---RESULT: PASS or FAIL
  ---CHECKS:
  - typecheck: PASS/FAIL (N errors)
  - lint: PASS/FAIL (N warnings/errors)
  - tests: PASS/FAIL (N passed, N failed)
  ---COVERAGE: XX% (or N/A)
  ---FAILURES:
  - description of each failure (if any, else write NONE)
  """
)
```

If `--single-agent` is set, the orchestrator runs verification itself.

### Verification outcomes

- If **PASS** → check coverage, then proceed to re-scoring (Phase 1 of next iteration)
- If **FAIL** → the orchestrator launches a new Fixer task instructed to undo the files listed in `FILES_MODIFIED`, then re-runs verification
- If **still failing after undo** → log the failure, keep the pre-fix state (no score update), and continue to the next iteration

### Coverage gate

After a passing verification, the orchestrator runs step 7 of the algorithm (see pseudocode):

- If coverage is available and drops more than 1% from the previous iteration, `PENDING_COVERAGE_DEBT` is set to `True`. The next Fixer must write tests before applying new logic fixes.
- If coverage recovers (no drop > 1%), `PENDING_COVERAGE_DEBT` is reset to `False`.
- If coverage is N/A for an iteration, `PENDING_COVERAGE_DEBT` is **not changed** — the debt status persists until coverage can be measured again.

The -1% tolerance avoids false positives from minor measurement variance.

## Phase 6: Re-Score and Loop

Go back to Phase 1 with a **fresh Reviewer Agent** (new subagent, no memory of previous review). This is critical — a fresh reviewer ensures the score is objective and not influenced by knowing what was fixed.

Display the iteration header and score progression:

```
╔══════════════════════════════════════╗
║  ITERATION 3 / 10        [3 agents] ║
║  Score: 79/100 (Grade B) ↑ +7       ║
║  Target: 85  |  Issues: 8 (was 15)  ║
║  P0: 0  P1: 2  P2: 4  P3: 2        ║
║                                      ║
║  History: 65 → 72 → 79              ║
╚══════════════════════════════════════╝
```

## Final Report

When the loop stops (for any reason), present the final report:

```
## COCO Fix Iterate — Final Report

### Result
- **Status: CONVERGED** (or: EXCELLENT / MAX_ITERATIONS / OSCILLATING / DIMINISHING / STALLED / STUCK)
- **Final Score: XX/100 (Grade X)**
- **Target: XX | Iterations: N/MAX**
- **Mode: multi-agent (3 agents/iteration)** or **single-agent**

### Score Progression

| Iter | Score | Delta | Coverage | Issues | Fixes Applied | Tests Written | Agents |
|------|-------|-------|----------|--------|---------------|---------------|--------|
| 1    | 65    | —     | 52%      | 15     | —             | —             | R+F+V  |
| 2    | 72    | +7    | 58%      | 11     | 4             | 2             | R+F+V  |
| 3    | 79    | +7    | 65%      | 8      | 3             | 2             | R+F+V  |
| 4    | 84    | +5    | 70%      | 5      | 3             | 1             | R+F+V  |
| 5    | 86    | +2    | 72%      | 3      | 2             | 1             | R+F+V  |

### Score Chart
  100 ┤
   90 ┤                          ●  target: 85
   80 ┤              ●     ●
   70 ┤        ●
   60 ┤  ●
      └────┬────┬────┬────┬────
           1    2    3    4    5

### Dimension Breakdown (Final)

| Dimension        | Start | Final | Change |
|------------------|-------|-------|--------|
| Correctness      | 60    | 95    | +35    |
| Security         | 40    | 90    | +50    |
| Test Coverage    | 50    | 85    | +35    |
| ...              | ...   | ...   | ...    |

### All Fixes Applied (N total)
- [x] P0: [file:line] Description
- [x] P1: [file:line] Description
- [x] P1: [file:line] Description
- ...

### Remaining Issues (N)
- P2: [file:line] Description
- P3: [file:line] Description

### Files Modified (N)
- path/to/file1.ts
- path/to/file2.ts

### Recommendations
- If score < target: "Run again with a higher --max-iterations or fix remaining P1 issues manually"
- If converged: "Code quality meets the target. Consider committing these changes."
```

## Important

- This skill runs **autonomously** — it does NOT pause for user confirmation between iterations
- It **does NOT commit** — all changes stay in the working tree for the user to review
- **Multi-agent is ON by default** — each iteration spawns 3 fresh subagents for objectivity
- Use `--single-agent` when you need speed over objectivity
- The default target score of **85** represents senior-level quality
- Use `--score 95` for production-critical code that needs excellent quality
- Use `--score 70` for prototypes or spikes where speed matters more
- If the score is stuck, the skill stops rather than making useless changes
- P3 (cosmetic) issues are **never fixed** in the loop to avoid unnecessary churn
- **Convergence requires 2 consecutive iterations at target, stable within 5 points**
- Each Reviewer Agent is **fresh** (no memory of previous iterations) to ensure unbiased scoring
- **The reviewer prompt must NEVER include previous scores or fix history** — this is the #1 source of false convergence
- **Recurring issues** (same file + description words) trigger escalated fix strategies, not repeated same attempts
- **Issue key format**: `"<file>:<first-6-words-of-description-slugified>"` — stable across line number shifts
- **Every P0/P1 logic fix must include a regression test** — the Fixer writes it, the Verifier confirms it passes
- **Coverage can only go up**: a drop of >1% between iterations sets `PENDING_COVERAGE_DEBT` — the next Fixer must add tests before new logic fixes
- After completion, the user can run `/code-review` to independently verify the final score
