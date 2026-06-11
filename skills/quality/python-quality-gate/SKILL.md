---
name: python-quality-gate
description: "Python quality checks: ruff, pytest, mypy, bandit in deterministic order."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
  - Skill
agent: python-general-engineer
routing:
  force_route: true
  not_for: "general Python coding (use python-general-engineer), data analysis scripts, or tutorials — fires when the user wants ruff/mypy/pytest/bandit quality checks run on existing code"
  triggers:
    - "Python quality"
    - "ruff check"
    - "bandit scan"
    - "mypy check"
    - "python lint"
    - "python quality gate"
    - "check python"
    - "pre-commit check"
  category: code-quality
  pairs_with:
    - code-linting
    - test-driven-development
---

# Python Quality Gate Skill

Run four quality tools in deterministic order -- ruff, pytest, mypy, bandit -- and produce a structured pass/fail report with severity-categorized issues and auto-fix commands.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| writing the quality gate report | `report-template.md` | Loads detailed guidance from `report-template.md`. |
| invoking ruff/mypy/pytest; severity classification and pass/fail thresholds | `tool-commands.md` | Loads detailed guidance from `tool-commands.md`. |

## Instructions

### Phase 1: Detection and Setup

**Step 1: Read CLAUDE.md and detect project configuration.**

Read and follow the repository's CLAUDE.md before any execution. Then detect project configuration:

```bash
ls -la pyproject.toml setup.py setup.cfg mypy.ini .python-version 2>/dev/null
```

Identify Python version target, ruff config, pytest config, mypy config from pyproject.toml. Only validate code -- never add tools, features, or flexibility not requested.

**Step 2: Detect source and test directories.**

```bash
ls -d src/ app/ lib/ 2>/dev/null || echo "Source: current directory"
ls -d tests/ test/ 2>/dev/null || echo "Tests: not found"
```

**Step 3: Verify tool availability.**

```bash
ruff --version
pytest --version
mypy --version || echo "mypy not installed (optional)"
bandit --version || echo "bandit not installed (optional)"
```

If ruff or pytest are missing, STOP. These are required:
```
ERROR: Required tool not found: {tool_name}
Install with: pip install ruff pytest pytest-cov
```

Do not install missing tools automatically unless the user explicitly requests it. Do not modify pyproject.toml or configuration files unless explicitly asked.

**Gate**: ruff and pytest available. Project structure identified. Proceed only when gate passes.

### Phase 2: Execute Quality Checks

Run all checks in fixed order, capturing full output for each. Show complete command output with exact file paths and line numbers -- never summarize or paraphrase tool output, because summarization hides the details engineers need to locate and fix issues.

**Step 1: Ruff linting.**

```bash
ruff check . --output-format=grouped
```

**Step 2: Ruff formatting check.**

```bash
ruff format --check .
```

**Step 3: Type checking with mypy** (if installed).

```bash
mypy . --ignore-missing-imports --show-error-codes
```

Skip and note in report if mypy is not installed. Even if tests pass, still run mypy when available -- tests check behavior while types check contracts, and passing one does not make the other redundant.

**Step 4: Run test suite.**

```bash
pytest -v --tb=short --cov=src --cov-report=term-missing
```

If no tests directory exists, skip and note in report. Never skip tests to make the gate pass -- tests verify functionality, and skipping them hides broken code. Only skip optional tools (mypy, bandit) if genuinely unavailable, not to manufacture a passing status.

**Step 5: Security scanning with bandit** (if installed).

```bash
bandit -r src/ -ll --format=screen
```

Skip and note in report if bandit is not installed. Linting passing does not mean code is correct -- linting finds style issues, not logic or security bugs. Run every available tool.

**Gate**: All available tools have been run. Full output captured. Proceed to analysis.

### Phase 3: Categorize and Analyze

**Step 1: Categorize issues by severity.**

See `references/tool-commands.md` for complete severity classification tables.

Summary of severity levels:
- **Critical**: F errors (pyflakes), E9xx (syntax), undefined names, test failures, high-severity security
- **High**: E501, E711/E712, F841, N8xx, arg-type/assignment mypy errors
- **Medium**: W warnings, C4xx, no-untyped-def mypy errors
- **Low**: SIM suggestions, UP upgrade suggestions

Always prioritize critical issues over style fixes -- critical issues (F errors, test failures) break functionality while style issues do not. Fix critical first, high second; use auto-fix for bulk style cleanup only after critical issues are resolved.

**Step 2: Count auto-fixable issues.**

```bash
ruff check . --statistics
```

Issues marked with `[*]` are auto-fixable. Show suggested auto-fix commands for these issues so users know what can be fixed automatically.

**Step 3: Determine overall status.**

FAIL if:
- Any ruff F errors or test failures
- Any high-severity bandit issues
- Mypy errors exceed 10 (configurable)
- Test coverage below 80% (if coverage enabled)

PASS otherwise. Exit with non-zero status if any critical check fails.

**Gate**: All issues categorized. Pass/fail determined. Proceed to report.

### Phase 4: Generate Report

Format a structured markdown report. See `references/report-template.md` for the full template.

The report MUST include:
1. Overall PASS/FAIL status
2. Summary table (each tool's status and issue count)
3. Total issues and auto-fixable count
4. Detailed results per tool (issues grouped by severity, then grouped by type and file for readability)
5. Critical issues requiring attention with file:line references
6. Auto-fix commands section
7. Quality metrics: error counts and coverage percentages

Report facts -- show raw command output rather than describing it. No self-congratulation ("great job", "looking good"). Generate the full report even when only style issues are found, because style issues can hide real problems in noise and a full severity-prioritized report surfaces them.

Print the complete report to stdout. Never summarize or truncate. If `--output {file}` flag was provided, also write report to file. Remove any intermediate temporary files at completion -- keep the final report only if the user requested file output.

**Gate**: Report generated and displayed. Task complete.

### Auto-Fix Mode (only when explicitly requested)

Auto-fix modifies files in place -- never run it without explicit user confirmation. Running `ruff --fix` blindly can change code semantics (import removal, reformatting), so always run check-only first, review issues, confirm auto-fix intent, then verify changes.

When user explicitly requests auto-fix:

```bash
ruff check . --fix
ruff format .
```

After auto-fix, show the diff so changes can be reviewed, then re-run the quality gate to verify:
```bash
git diff
```

## Examples

### Example 1: Pre-Merge Quality Check
User says: "Run quality checks before I merge this PR"
Actions:
1. Detect project config and available tools (Phase 1)
2. Run ruff check, ruff format, mypy, pytest, bandit in order (Phase 2)
3. Categorize 12 issues: 0 critical, 3 high, 9 medium (Phase 3)
4. Generate report showing PASSED with 3 high-priority suggestions (Phase 4)
Result: Structured report with actionable fix commands

### Example 2: Quality Gate Failure
User says: "Check code quality on the payments module"
Actions:
1. Detect config, find src/payments/ directory (Phase 1)
2. Run all tools -- pytest shows 2 failures, ruff finds F401 errors (Phase 2)
3. Categorize: 2 critical (test failures), 1 critical (undefined name), 5 medium (Phase 3)
4. Generate FAILED report with critical issues listed first (Phase 4)
Result: FAILED status with prioritized fix list, auto-fix commands for 5 medium issues

## Error Handling

### Error: "ruff: command not found"
**Cause**: Ruff is not installed in the current environment
**Solution**: Install with `pip install ruff`. Do not proceed without ruff -- exit with status 2.

### Error: "Tests failed with exit code 1"
**Cause**: pytest found test failures
**Solution**: This is expected behavior, not a tool error. Parse output, include failure details in report, mark overall status as FAILED, continue with remaining checks.

### Error: "No Python files found"
**Cause**: Running from wrong directory or not a Python project
**Solution**: Verify location with `ls pyproject.toml src/ tests/`. Run from project root.

### Error: "Mypy cache corruption"
**Cause**: Stale or corrupted .mypy_cache directory
**Solution**: Clear cache with `rm -rf .mypy_cache` and retry. If mypy continues to fail, skip type checking and note in report.

## References

### Reference Files
- `${CLAUDE_SKILL_DIR}/references/tool-commands.md`: Severity classifications, expected output formats, CLI flags
- `${CLAUDE_SKILL_DIR}/references/report-template.md`: Full structured report template
- `${CLAUDE_SKILL_DIR}/references/pyproject-template.toml`: Complete ruff, pytest, mypy, bandit configuration
