---
name: parallel-validator
description: "Run validation suite in parallel background workers. Auto-triggered after code changes when multiple validators apply. Use when tests, lint, and security checks should run simultaneously."
allowed-tools: Task, Bash, Read, Glob
---

# Parallel Validator

Run multiple validation tasks (tests, lint, security) in parallel background workers to minimize wait time and keep main context clean.

## When To Use

**Auto-Trigger Signals:**
- Code changes complete and ready for validation
- Multiple validators applicable (tests + lint + security)
- Before commit/PR creation
- User says "validate", "check everything", "run all checks"

**Skip When:**
- Only one validator needed (use that skill directly)
- Quick single-file change (overhead not worth it)
- User needs real-time feedback on specific test

## Inputs

- Code changes to validate
- Which validators to run (auto-detected or specified)
- Pass/fail thresholds

## Outputs

- Aggregated pass/fail status
- Summary of issues by severity
- Detailed results available on request

---

## Validator Detection

Auto-detect applicable validators by checking for config files:

| Validator | Detection | Agent |
|-----------|-----------|-------|
| Tests (Python) | pytest.ini, pyproject.toml, tests/ | background-worker |
| Tests (JS) | jest.config.*, vitest.config.* | background-worker |
| Tests (Go) | *_test.go files | background-worker |
| Lint (Python) | ruff.toml, .flake8, pylintrc | background-worker |
| Lint (JS) | .eslintrc*, prettier.config.* | background-worker |
| Type Check | tsconfig.json, mypy.ini | background-worker |
| Security | Any code changes | security-auditor |

---

## Parallel Execution Pattern

### Step 1: Detect Validators

```bash
# Check what's available
ls pytest.ini pyproject.toml 2>/dev/null && echo "pytest"
ls jest.config.* vitest.config.* 2>/dev/null && echo "jest"
ls .eslintrc* 2>/dev/null && echo "eslint"
ls tsconfig.json 2>/dev/null && echo "typescript"
```

### Step 2: Spawn All in Parallel

In a SINGLE message, spawn all validators as background tasks:

```
# Spawn all in one message (parallel execution)
Task:
  subagent_type: background-worker
  description: "Run pytest"
  prompt: "Run pytest with -v flag. Return pass/fail count and any failures."
  run_in_background: true

Task:
  subagent_type: background-worker
  description: "Run ESLint"
  prompt: "Run eslint on src/. Return error count and top 5 issues."
  run_in_background: true

Task:
  subagent_type: security-auditor
  description: "Security scan"
  prompt: "Scan for OWASP top 10, secrets, auth issues. Return severity-ranked findings."
  run_in_background: true
```

### Step 3: Continue Work (Optional)

While validators run, you can continue with other tasks if applicable.

### Step 4: Poll for Results

```
# Check all validators (can poll in parallel too)
TaskOutput: { task_id: "pytest_id", block: true }
TaskOutput: { task_id: "eslint_id", block: true }
TaskOutput: { task_id: "security_id", block: true }
```

### Step 5: Aggregate and Report

```markdown
## Validation Results

| Validator | Status | Summary |
|-----------|--------|---------|
| pytest | PASS | 42 tests passed |
| eslint | WARN | 3 warnings (no errors) |
| security | PASS | No vulnerabilities found |

**Overall: READY FOR COMMIT**
```

---

## Failure Handling

### Critical Failures (Block Commit)
- Test failures
- Security vulnerabilities (HIGH/CRITICAL)
- Type errors

### Warnings (Allow Commit with Note)
- Lint warnings
- Low-severity security findings
- Coverage below threshold (but not failing)

### Action on Failure

```
1. Report which validators failed
2. Show specific failures (not full output)
3. Ask: "Fix issues or commit anyway?"
4. If fix: Address failures, re-run only failed validators
5. If commit anyway: Document skipped checks in commit message
```

---

## Context Efficiency

| Traditional | Parallel Validator |
|-------------|-------------------|
| Run pytest (wait 30s) | Spawn 3 agents (instant) |
| Run eslint (wait 10s) | Continue other work |
| Run security (wait 20s) | Poll when ready |
| **Total: 60s sequential** | **Total: 30s parallel** |
| **Context: Full output** | **Context: Summary only** |

### Token Savings

Each validator agent:
- Runs in isolated context
- Only returns summary (not full logs)
- ~200 tokens per validator returned to main

vs Traditional:
- Full pytest output (5000+ tokens)
- Full eslint output (2000+ tokens)
- Full security report (3000+ tokens)

**Savings: 90%+ context reduction**

---

## Integration with Other Skills

### With implement-plan
After each task group completion, trigger parallel-validator:
```
Task group complete → parallel-validator → report → next group
```

### With git-workflow
Before commit/PR, auto-run:
```
git add → parallel-validator → if pass → commit
```

### With beads
Track validator runs as agent tasks:
```bash
bd create "Validation run" -t agent_task --meta '{"validators": ["pytest", "eslint", "security"]}'
```

---

## Command Shortcuts

```bash
# Validate everything
/parallel-validator

# Validate specific
/parallel-validator tests,lint

# Validate with coverage
/parallel-validator --with-coverage

# Quick validation (skip security)
/parallel-validator --quick
```

---

## Anti-Patterns

- Running validators sequentially when parallel is possible
- Waiting for each validator before starting next
- Including full test output in main context
- Re-running all validators when only one failed
- Skipping security check to save time

---

## Keywords

parallel, validate, tests, lint, security, background, concurrent, pre-commit, ci, check
