---
name: fixing-code
description: Fix ALL issues via parallel agents with zero tolerance quality enforcement. Use when user says "fix", "fix issues", "fix errors", "fix all", "fix bugs", "fix lint", "fix tests", or wants to resolve code problems.
user-invocable: true
context: fork
argument-hint: "[team]"
allowed-tools:
  - Task
  - TaskOutput
  - TodoWrite
  - Bash(make *)
  - Bash(go *)
  - Bash(golangci-lint *)
  - Bash(pytest *)
  - Bash(ruff *)
  - Bash(npm *)
  - Bash(bun *)
  - Bash(bunx *)
---

# Fix All Issues

Execute until clean. Parallel analysis, sequential fixes.

**Parse `$ARGUMENTS`:**

- `team` → Agent team mode: Analysts compete to find root causes and debate solutions

**Use TodoWrite** to track these 5 phases:

1. Run validation
2. Parallel analysis (spawn agents or team)
3. Collect analysis results
4. Sequential fixes
5. Final verification

---

## Phase 1: Run Validation

```bash
make lint 2>&1 | head -100
make test 2>&1 | head -100
```

No Makefile? Detect language and run:

- **Go**: `golangci-lint run ./... 2>&1 | head -100 && go test -race ./... 2>&1 | head -100`
- **Python**: `ruff check . 2>&1 | head -100 && pytest 2>&1 | head -100`
- **TypeScript**: `bun lint 2>&1 | head -100 && bun test 2>&1 | head -100`
- **Web (HTML/CSS/JS)**: `bunx html-validate "**/*.html" 2>&1 | head -50 && bunx stylelint "**/*.css" 2>&1 | head -50 && bunx eslint "**/*.js" 2>&1 | head -50`

**If all pass**: Report "All checks pass" → stop.

---

## Phase 2: Parallel Analysis (Read-Only)

### Analysis Mode

**If `team` NOT in `$ARGUMENTS`** (Subagent mode - default):

Spawn ALL relevant language agents IN ONE MESSAGE for parallel execution.

**If `team` in `$ARGUMENTS`** (Team mode):

Create an agent team where analysts compete to find root causes and debate solutions. This mode is better for complex or mysterious issues where multiple perspectives help.

---

### Subagent Mode (Default)

Based on detected languages with issues, spawn analysis agents:

```
Task(
  subagent_type="go-qa",
  run_in_background=true,
  description="Go issue analysis",
  prompt="Analyze these Go issues. DO NOT FIX - analysis only.
  Issues:
  {lint/test output}

  Return structured analysis:
  - Root cause for each issue
  - Suggested fix approach
  - File:line references
  - Priority (critical/important/minor)"
)

Task(
  subagent_type="py-qa",
  run_in_background=true,
  description="Python issue analysis",
  prompt="Analyze these Python issues. DO NOT FIX - analysis only.
  Issues:
  {lint/test output}

  Return structured analysis:
  - Root cause for each issue
  - Suggested fix approach
  - File:line references
  - Priority (critical/important/minor)"
)

Task(
  subagent_type="web-qa",
  run_in_background=true,
  description="Web frontend issue analysis",
  prompt="Analyze these web frontend issues. DO NOT FIX - analysis only.
  Issues:
  {lint/test output}

  Return structured analysis:
  - Root cause for each issue
  - Suggested fix approach
  - File:line references
  - Priority (critical/important/minor)"
)
```

### Team Mode (If `team` in Arguments)

Create an agent team for competing analysis:

```
Create an agent team to analyze these issues. Spawn analysts for each language:

{If Go issues}:
- go-qa: Analyze Go issues from security/performance angle
- go-impl: Analyze from implementation/architecture angle
- go-tests: Analyze from testability angle

{If Python issues}:
- py-qa: Analyze Python issues from security/performance angle
- py-impl: Analyze from implementation angle
- py-tests: Analyze from test perspective

{If TypeScript issues}:
- ts-qa: Analyze TypeScript issues from security/performance angle
- ts-impl: Analyze from implementation angle
- ts-tests: Analyze from test perspective

{If Web issues}:
- web-qa: Analyze from security/performance/a11y angle
- web-impl: Analyze from implementation angle

Have analysts:
1. Independently diagnose root causes
2. Compete to find the most likely explanation
3. Debate proposed solutions
4. Challenge each other's assumptions
5. Converge on consensus root cause + fix approach

Return prioritized list with confidence levels and dissenting opinions.
```

The team lead will synthesize competing analyses into prioritized action plan.

---

## Phase 3: Collect Analysis Results

```
TaskOutput(task_id=<go_qa_id>, block=true)
TaskOutput(task_id=<py_qa_id>, block=true)
TaskOutput(task_id=<web_qa_id>, block=true)
```

Merge and prioritize issues:

1. Critical (blocking): Fix first
2. Important (quality): Fix second
3. Minor (style): Fix if time permits

---

## Phase 4: Sequential Fixes

**Fix issues ONE AT A TIME to avoid conflicts:**

For each issue (prioritized order):

1. Read the file
2. Apply fix using Edit tool
3. Verify fix didn't break anything: `make lint && make test` or equivalent

**If fix causes new issues**: Revert and try alternative approach.

---

## Phase 5: Final Verification

```bash
make lint && make test
```

**Loop back to Phase 2** if issues remain.

---

## Exit Criteria

- Build passes
- All tests pass
- Zero lint errors

## Output

```
FIX COMPLETE
============
Mode: {Subagent Analysis | Team Analysis}
Analysis: {N} issues identified by {M} agents
Fixed: {X} issues
Remaining: {Y} non-blocking (if any)
Status: CLEAN | NEEDS ATTENTION

Changes:
- file1.go:42 - Fixed null pointer check
- file2.py:15 - Added missing type hint
```

## Examples

```
/fixing-code           # Subagent mode: parallel analysis
/fixing-code team      # Team mode: competing analysis with debate
```

---

**Execute validation now.**
