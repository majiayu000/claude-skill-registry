---
name: quality-run-quality-gates
description: Enforce Definition of Done by running quality gates (type checking, linting, dead code detection, tests). Use when task is complete, before commits, when declaring "done", or when user says "check all", "run quality gates", "validate code quality", or "run tests and linting". Adapts to Python (pyright/ruff/vulture/pytest), JavaScript (tsc/eslint/jest), and other ecosystems. MANDATORY before marking tasks complete.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Run Quality Gates

## Purpose

Enforce Definition of Done by detecting and running all quality gates (type checking, linting, dead code detection, tests) for Python, JavaScript, Go, Rust, and other ecosystems. Provides actionable feedback for failures and blocks task completion until all gates pass.

## Table of Contents

**Quick Start** → [When to Use](#when-to-use-this-skill) | [What It Does](#what-this-skill-does) | [Simple Example](#quick-start)

**How to Implement** → [Detection Process](#quality-gate-detection) | [Execution Workflow](#execution-workflow) | [Outcomes](#expected-outcomes)

**Automation** → [Scripts](scripts/) | [Templates](templates/) | [Supporting Files](#supporting-files)

**Help** → [Anti-Patterns](#anti-pattern-prevention) | [Output Format](#output-format) | [Integration](#integration-with-existing-tools)

**Reference** → [Tool Reference](references/quality-gate-tools.md) | [Common Failures](references/common-failures.md)

---

## When to Use This Skill

**MANDATORY in these situations:**
- Before declaring a task "done" or "complete"
- Before marking a todo as completed
- Before creating a commit or pull request
- When user says "check all", "run quality gates", "validate code"
- After implementing new features or bug fixes
- After refactoring code

**User trigger phrases:**
- "run quality gates"
- "check all"
- "run tests and linting"
- "validate code quality"
- "is this done?"
- "run checks"
- "check before commit"

**Additional detection patterns:**
- After manually running individual tools (e.g., "I ran ruff check")
- When user says "I fixed linting" but hasn't run other gates
- After code changes but before marking task complete
- When only partial quality checks were performed

## What This Skill Does

Enforces the **Definition of Done** by:

1. **Detecting project type** (Python, JavaScript, TypeScript, etc.)
2. **Identifying quality gate tools** (check_all.sh script or individual tools)
3. **Running all quality gates** in parallel when possible
4. **Capturing and categorizing failures** (type errors, lint errors, dead code, test failures)
5. **Providing actionable fixes** for each failure category
6. **Re-running gates** after fixes until all pass
7. **Confirming zero errors** before declaring success

**Result:** ✅ All gates pass (task truly done) or ❌ Failures (with specific fixes needed)

## Quick Start

### Example 1: Task Completion Check

```
User: "I'm done implementing the new feature"

Claude invokes skill:
→ Detects Python project with check_all.sh
→ Runs: ./scripts/check_all.sh
→ Reports results

Output:
✅ All 6 checks passed (pyright, vulture, pytest, ruff, ruff format, ty)
✅ DEFINITION OF DONE: MET
Task is complete and ready for commit.
```

### Example 2: Failures Detected

```
User: "Run quality gates"

Claude invokes skill:
→ Runs quality gates
→ Detects 3 failures

Output:
❌ 3 of 6 checks failed: pyright, pytest, ruff

📋 pyright failures (3 errors):
  src/services/search.py:45 - Type "None" cannot be assigned to "str"
  src/utils/helper.py:12 - Argument of type "int" cannot be assigned to "Optional[str]"

📋 pytest failures (2 errors):
  tests/unit/test_search.py::test_search_empty - AssertionError

📋 ruff failures (1 error):
  src/services/search.py:23 - F401 Unused import: logging

Next steps:
1. Fix type errors (make parameters non-optional)
2. Fix test assertions
3. Remove unused imports
4. Re-run quality gates

❌ DEFINITION OF DONE: NOT MET
Task is NOT complete until all gates pass.
```

## Instructions

### Overview

Running quality gates involves 5 key steps:

1. **Detect project type and tools** - Identify language and available quality gate tools
2. **Run quality gates** - Execute all gates (unified script or individual tools)
3. **Parse results** - Categorize failures by type (type errors, lint, tests, dead code)
4. **Provide actionable fixes** - Generate specific fix recommendations for each failure
5. **Re-run after fixes** - Validate that all issues are resolved

See detailed workflow in [Execution Workflow](#execution-workflow) section below.

## Quality Gate Detection

### Detection Process

1. **Check for unified script** (preferred):
   - `./scripts/check_all.sh` (Python projects)
   - `npm run check` (JavaScript/TypeScript projects)
   - `make check` (Makefile-based projects)

2. **Fallback to individual tools** by detecting project type:

#### Python Projects
Detect via: `pyproject.toml`, `requirements.txt`, `setup.py`

Tools to run:
- **Type checking:** `uv run pyright` or `mypy`
- **Linting:** `uv run ruff check` or `pylint` or `flake8`
- **Dead code:** `uv run vulture src/ --min-confidence 80`
- **Tests:** `uv run pytest tests/ -q`
- **Formatting:** `uv run ruff format --check` or `black --check`

#### JavaScript/TypeScript Projects
Detect via: `package.json`, `tsconfig.json`

Tools to run:
- **Type checking:** `npx tsc --noEmit`
- **Linting:** `npx eslint src/`
- **Tests:** `npm test` or `npx jest` or `npx vitest`
- **Formatting:** `npx prettier --check src/`

#### Go Projects
Detect via: `go.mod`

Tools to run:
- **Type checking:** `go build ./...`
- **Linting:** `golangci-lint run`
- **Tests:** `go test ./...`
- **Formatting:** `go fmt ./...`

#### Rust Projects
Detect via: `Cargo.toml`

Tools to run:
- **Type checking:** `cargo check`
- **Linting:** `cargo clippy`
- **Tests:** `cargo test`
- **Formatting:** `cargo fmt --check`

### Project-Specific Configuration

Read project-specific quality gates from:
- `CLAUDE.md` (Definition of Done section)
- `pyproject.toml` (Python)
- `package.json` (JavaScript/TypeScript)
- `.pre-commit-config.yaml` (Pre-commit hooks)

## Execution Workflow

### Step 1: Detect Project and Tools

```bash
# Check for unified script
if [ -f ./scripts/check_all.sh ]; then
    RUNNER="./scripts/check_all.sh"
elif [ -f package.json ] && grep -q '"check"' package.json; then
    RUNNER="npm run check"
elif [ -f Makefile ] && grep -q "^check:" Makefile; then
    RUNNER="make check"
else
    # Fallback to individual tools (detect project type)
    ...
fi
```

### Step 2: Run Quality Gates

```bash
# Run unified script or individual tools
$RUNNER

# Capture output and exit code
EXIT_CODE=$?
```

### Step 3: Parse and Categorize Failures

Extract failures by tool:
- **Type errors:** Lines matching `error:` or `error[`
- **Lint errors:** Lines matching `.py:line:col:` or `.js:line:col:`
- **Dead code:** Lines matching `unused` or `dead code`
- **Test failures:** Lines matching `FAILED` or `ERROR collecting`

### Step 4: Provide Actionable Fixes

For each failure category, provide:
1. **File:line reference** (exact location)
2. **Error description** (what's wrong)
3. **Suggested fix** (how to resolve)
4. **Priority** (HIGH/MEDIUM/LOW based on error type)

### Step 5: Re-run After Fixes

After user applies fixes:
```bash
# Re-run quality gates
$RUNNER

# Verify all pass
if [ $? -eq 0 ]; then
    echo "✅ All quality gates passed"
    echo "✅ DEFINITION OF DONE: MET"
else
    echo "❌ Some gates still failing"
    # Repeat steps 3-4
fi
```

## Anti-Pattern Prevention

### ❌ Anti-Pattern 1: Declaring Done Without Running Gates

**User:** "I'm done with the feature"

**Wrong Response:**
```
✅ Great! The feature is complete.
```

**Correct Response (Invoke Skill):**
```
Let me verify the feature meets Definition of Done by running quality gates...

→ Runs quality gates
→ Reports results (pass/fail)
→ Only declares "done" if all gates pass
```

### ❌ Anti-Pattern 2: Ignoring Quality Gate Failures

**User:** "Some tests are failing but the main logic works"

**Wrong Response:**
```
✅ The core functionality is complete. The test failures are minor.
```

**Correct Response:**
```
❌ DEFINITION OF DONE: NOT MET

Quality gates must pass before declaring done:
- 2 tests failing in tests/unit/test_search.py
- 1 type error in src/services/search.py

Let me fix these issues...
[Proceeds to fix each failure]
```

### ❌ Anti-Pattern 3: "Will Fix Later" Mentality

**User:** "Let's commit this and fix the lint errors later"

**Wrong Response:**
```
✅ Creating commit...
```

**Correct Response:**
```
❌ Cannot commit - quality gates failing:
- 3 ruff lint errors
- 1 unused import

Project policy: All gates must pass before commit.
Let me fix these now (takes ~30 seconds)...
```

### ❌ Anti-Pattern 4: Skipping Tests

**User:** "I added the feature but didn't write tests yet"

**Wrong Response:**
```
✅ Feature added successfully.
```

**Correct Response:**
```
⚠️ DEFINITION OF DONE: INCOMPLETE

Feature implemented but missing:
- Unit tests for new functionality
- Integration tests for end-to-end flow

Project policy: Tests required before declaring done.
Let me add tests now...
```

### ❌ Anti-Pattern 5: Partial Quality Check (NEW)

**User:** "I ran ruff check and fixed all linting errors"

**Wrong Response:**
```
✅ Code quality verified - all linting issues resolved.
```

**Correct Response:**
```
⚠️ PARTIAL QUALITY CHECK DETECTED

You ran: ruff check ✅ (linting passed)
Missing: type checking, tests, dead code detection

Running complete quality gate suite...
→ pyright (type checking)
→ pytest (tests)
→ vulture (dead code)
→ ruff format (formatting)

[Runs all gates and reports results]
```

**Detection signals:**
- User mentions running only ONE tool (ruff, eslint, tsc, etc.)
- User says "fixed linting" but no mention of tests/types
- Only one command executed (e.g., `ruff check --fix`)
- No mention of running `check_all.sh` or equivalent

**Why this matters:**
Linting alone doesn't verify:
- ❌ Type safety (pyright/mypy catch type errors)
- ❌ Correctness (pytest catches logic errors)
- ❌ Unused code (vulture detects dead code)
- ❌ Formatting consistency (ruff format)

**Real-world example:**
```
User ran: ruff check --fix
Missed issues:
- 3 type errors in src/layout_io.py (pyright would catch)
- 1 failing test in tests/test_save.py (pytest would catch)
- 2 unused imports (ruff found but user only ran check, not full suite)
```

## Output Format

### Success Output

```
🚦 Quality Check Results
──────────────────────────────────────────────────
✅ pyright [2s]
✅ vulture [1s]
✅ pytest [3s]
✅ ruff [1s]
✅ ruff format [1s]
✅ ty [2s]
──────────────────────────────────────────────────
✅ All 6 checks passed

✅ DEFINITION OF DONE: MET
- All type checks passed
- All linting passed
- All tests passed (100% pass rate)
- No dead code detected
- Code formatting correct

Task is complete and ready for commit.
```

### Failure Output with Fixes

```
🚦 Quality Check Results
──────────────────────────────────────────────────
❌ pyright [2s]

📋 pyright failures:
  src/services/search.py:45 - error: Type "None" cannot be assigned to type "str"
  src/utils/helper.py:12 - error: Argument of type "int" cannot be assigned to parameter of type "Optional[str]"

❌ pytest [3s]

📋 pytest failures:
  FAILED tests/unit/test_search.py::test_search_empty - AssertionError: Expected [] but got None

❌ ruff [1s]

📋 ruff failures:
  src/services/search.py:23 - F401 [*] `logging` imported but unused

──────────────────────────────────────────────────
❌ 3 of 6 checks failed: pyright, pytest, ruff

❌ DEFINITION OF DONE: NOT MET

Required fixes:
1. Type Errors (HIGH priority):
   - src/services/search.py:45 - Make return type non-optional or handle None case
   - src/utils/helper.py:12 - Convert int to str or change parameter type

2. Test Failures (HIGH priority):
   - tests/unit/test_search.py::test_search_empty - Update assertion to handle None case

3. Lint Errors (MEDIUM priority):
   - src/services/search.py:23 - Remove unused logging import

Next steps:
1. Fix each issue systematically (start with HIGH priority)
2. Re-run quality gates after each fix
3. Repeat until all gates pass
```

## Integration with Existing Tools

### With check_all.sh Script

If project has `./scripts/check_all.sh`:
```bash
# Skill detects script and uses it directly
./scripts/check_all.sh

# Parses output (already formatted for agent consumption)
# Returns structured results
```

### With Pre-Commit Hooks

Skill can be invoked by pre-commit hooks:
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: quality-gates
      name: Run Quality Gates
      entry: claude-skill run-quality-gates
      language: system
      pass_filenames: false
```

### With TodoWrite Tool

Before marking todo as completed:
```python
# ❌ WRONG - Mark completed without validation
TodoWrite([{"content": "Implement search", "status": "completed"}])

# ✅ CORRECT - Validate first
run_quality_gates()  # Invoke skill
if all_gates_pass:
    TodoWrite([{"content": "Implement search", "status": "completed"}])
```

### With Agent Workflows

Agents should invoke this skill before declaring tasks complete:
```
@implementer completes feature implementation
→ @implementer invokes run-quality-gates skill
→ Skill runs all gates
→ If pass: Mark todo as completed
→ If fail: Fix issues, re-run gates
```

## Configuration

### Project-Specific Quality Gates

Projects can define custom quality gates in `CLAUDE.md`:

```markdown
## Quality Gates (MANDATORY)

Run before saying "done":

```bash
./scripts/check_all.sh  # Runs all checks in parallel
```

Individual checks if needed:
```bash
uv run pyright          # Type checking
uv run vulture src/     # Dead code detection
uv run pytest tests/    # Test suite
uv run ruff check src/  # Linting
```

**Non-negotiable:** Task is NOT done if quality gates fail. Fix or explain why.
```

Skill will read this section and use the specified commands.

### Custom Tool Detection

For projects with non-standard setups, create `.claude/quality-gates.json`:

```json
{
  "runner": "./custom_check_script.sh",
  "tools": {
    "type_checker": "uv run pyright",
    "linter": "uv run ruff check",
    "dead_code": "uv run vulture src/",
    "tests": "uv run pytest tests/",
    "formatter": "uv run ruff format --check"
  },
  "required": ["type_checker", "linter", "tests"],
  "optional": ["dead_code", "formatter"]
}
```

## Expected Outcomes

### Outcome 1: All Gates Pass

```
✅ All 6 checks passed
✅ DEFINITION OF DONE: MET
Task is complete and ready for commit.
```

**Agent response:**
- Marks todo as completed
- Creates commit if requested
- Declares task done

### Outcome 2: Some Gates Fail

```
❌ 3 of 6 checks failed: pyright, pytest, ruff
❌ DEFINITION OF DONE: NOT MET
```

**Agent response:**
- Does NOT mark todo as completed
- Provides specific fixes for each failure
- Re-runs gates after fixes
- Repeats until all pass

### Outcome 3: Persistent Failures

```
❌ After 3 fix attempts, 1 gate still failing
❌ Type error may require architectural change
```

**Agent response:**
- Escalates to user
- Explains root cause
- Suggests options:
  1. Make architectural change
  2. Update test expectations
  3. Request guidance

### Outcome 4: No Quality Gate Tools Found

```
⚠️ No quality gate tools detected
⚠️ Cannot validate Definition of Done
```

**Agent response:**
- Asks user which tools to use
- Suggests standard tools for detected project type
- Offers to create check_all.sh script

## Supporting Files

- [references/shared-quality-gates.md](references/shared-quality-gates.md) - Shared quality gates documentation and patterns
- [references/quality-gate-tools.md](references/quality-gate-tools.md) - Complete list of tools by ecosystem
- [references/common-failures.md](references/common-failures.md) - Common failure patterns and fixes
- [references/detection-rules.md](references/detection-rules.md) - How to detect project type and tools
- [templates/check_all_template.sh](templates/check_all_template.sh) - Template for creating check_all.sh

## Utility Scripts

- [Detect Quality Gates Script](./scripts/detect_quality_gates.sh) - Tool detection script

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Gates run before declaring "done" | 100% | TBD |
| False "done" declarations | 0% | TBD |
| Quality gate pass rate | 100% | TBD |
| Time to run gates | <10s | TBD |
| Fix accuracy (first attempt) | >80% | TBD |

## Usage Examples

### Example 1: Pre-Commit Quality Check

```bash
# User: "I'm done implementing the feature"
# Skill invocation:
Skill(command: "run-quality-gates")

# Output: All gates pass, ready to commit
✅ All 6 checks passed
✅ DEFINITION OF DONE: MET
```

### Example 2: Failed Gates with Fixes

```bash
# User: "Run quality gates"
# Skill invocation:
Skill(command: "run-quality-gates")

# Output: 3 failures with specific fixes
❌ 3 of 6 checks failed
Fix pyright errors, pytest failures, ruff violations
```

## Troubleshooting

### Issue: Quality gates take too long (>5 minutes)

**Solution:**
```bash
# Use optimized check_all.sh (runs in parallel: 8s vs 31s)
./scripts/check_all.sh

# For incremental changes, run only affected checks
uv run pyright --files-changed
uv run ruff check --diff
```

### Issue: False positives from vulture

**Solution:**
```bash
# Add exclusions to pyproject.toml
[tool.vulture]
exclude = ["tests/", "*.pyi"]
min_confidence = 80
```

### Issue: Tests pass locally but fail in CI

**Solution:**
```bash
# Ensure same environment
uv sync
uv run pytest tests/ -v

# Check for environment-specific issues
# - Database connections
# - File paths
# - Network dependencies
```

## Additional Resources

See [Troubleshooting](#troubleshooting) and [Usage Examples](#usage-examples) sections above for comprehensive guidance including:
- Python project with check_all.sh
- JavaScript project with npm scripts
- Go project with Makefile
- Multi-language monorepo
- Project without existing quality gates

## Integration Points

### With Other Skills

**run-quality-gates integrates with:**
- **git-commit-push** - MANDATORY integration before any commit
- **code-review** - Invoked as Step 7 of code review process
- **detect-quality-regressions** - Uses quality gate results for regression detection
- **capture-quality-baseline** - Establishes baseline metrics for comparison

### With Agent Workflows

**Agents should invoke this skill:**
- @implementer - Before marking tasks complete
- @code-review-expert - During pre-commit review
- @debugging-expert - After fixing bugs to verify quality

### With TodoWrite Tool

**Integration pattern:**
```python
# Before marking todo as completed
run_quality_gates()  # Invoke skill
if all_gates_pass:
    TodoWrite([{"content": "Task", "status": "completed"}])
else:
    # Fix issues first
    pass
```

## Expected Benefits

| Metric | Without Quality Gates | With Quality Gates | Improvement |
|--------|----------------------|-------------------|-------------|
| Bugs in production | 15-20 per release | 2-3 per release | 85% reduction |
| Time to fix bugs | 2-4 hours | 15-30 min | 75% faster |
| Code review time | 30-60 min | 10-20 min | 60% faster |
| Test coverage | 60-70% | 85-95% | 30% increase |
| Merge conflicts | 5-10 per week | 1-2 per week | 80% reduction |
| Rework after review | 40-60% of PRs | 5-10% of PRs | 85% reduction |

## Requirements

**No external dependencies** - Skill adapts to whatever tools are already installed in the project.

**Minimum requirements:**
- Bash shell (for running scripts)
- Read access to project files (for detection)
- Execute permissions on quality gate scripts

**Optional:**
- `CLAUDE.md` with Definition of Done section (for custom configuration)
- `.claude/quality-gates.json` (for explicit tool specification)
