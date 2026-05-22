---
name: fixing-code
description: Fix ALL issues via parallel agents with zero tolerance quality enforcement. Use when user says "fix", "fix issues", "fix errors", "fix all", "fix bugs", "fix lint", "fix tests", or wants to resolve code problems.
user-invocable: true
context: fork
allowed-tools:
  - Task
  - TaskOutput
  - TodoWrite
  - Bash(make:*)
  - Bash(go:*)
  - Bash(golangci-lint:*)
  - Bash(pytest:*)
  - Bash(ruff:*)
  - Bash(npm:*)
  - Bash(bun:*)
  - Bash(bunx:*)
---

# Fix All Issues

Execute until clean. Parallel analysis, sequential fixes.

**Use TodoWrite** to track these 5 phases:

1. Run validation
2. Parallel analysis (spawn agents)
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

**Spawn ALL relevant language agents IN ONE MESSAGE for parallel execution:**

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
Analysis: {N} issues identified by {M} agents
Fixed: {X} issues
Remaining: {Y} non-blocking (if any)
Status: CLEAN | NEEDS ATTENTION

Changes:
- file1.go:42 - Fixed null pointer check
- file2.py:15 - Added missing type hint
```

---

**Execute validation now.**
