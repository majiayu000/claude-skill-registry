---
name: tdd-enforce
description: Configure TDD enforcement via pre-commit hooks and CI coverage gates. Use when setting up test-first development workflow, adding coverage gates, or enforcing TDD practices.
version: 1.0.0
---

# TDD Enforce Skill

## Purpose

Configure Test-Driven Development enforcement through pre-commit hooks, CI coverage gates, and automated test execution. Ensures code cannot be committed or merged without adequate test coverage.

## Research Foundation

| Principle | Source | Reference |
|-----------|--------|-----------|
| TDD Methodology | Kent Beck (2002) | "Test-Driven Development by Example" |
| 80% Coverage | Google Testing Blog (2010) | [Code Coverage Goal](https://testing.googleblog.com/2010/07/code-coverage-goal-80-and-no-less.html) |
| Pre-commit Hooks | Industry Best Practice | [Husky](https://typicode.github.io/husky/), [pre-commit](https://pre-commit.com/) |
| CI Gates | ISTQB CT-TAS | [Test Automation Strategy](https://istqb.org/certifications/certified-tester-test-automation-strategy-ct-tas/) |

## When This Skill Applies

- User asks to "set up TDD" or "enforce test-first"
- User wants to "add coverage gates" or "block commits without tests"
- User mentions "pre-commit hooks for tests" or "CI test gates"
- Project needs test quality enforcement
- Brownfield project needs TDD adoption

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Set up TDD enforcement" | Configure pre-commit + CI gates |
| "Add coverage gates" | Configure CI coverage thresholds |
| "Block commits without tests" | Set up pre-commit test hooks |
| "Enforce test-first development" | Full TDD setup |
| "Run tests on commit" | Configure pre-commit test execution |
| "Check if tests exist for new code" | Configure test presence validation |

## Configuration Options

### Coverage Thresholds

```yaml
coverage:
  line: 80        # Google standard: 80% minimum
  branch: 75      # Branch coverage threshold
  function: 90    # Function coverage threshold
  critical_paths: 100  # Auth, payments, validation
```

### Enforcement Levels

| Level | Pre-commit | CI Gate | Description |
|-------|-----------|---------|-------------|
| `strict` | Block | Fail | No exceptions, 100% enforcement |
| `standard` | Warn + Block | Fail | Standard TDD enforcement |
| `gradual` | Warn | Warn | For TDD adoption in brownfield |
| `audit` | Log only | Report | Visibility without blocking |

## Implementation Process

### 1. Detect Project Type

```python
def detect_project():
    """Identify project language and tooling"""
    if exists("package.json"):
        return "javascript"  # Use Husky
    elif exists("pyproject.toml") or exists("setup.py"):
        return "python"      # Use pre-commit
    elif exists("pom.xml") or exists("build.gradle"):
        return "java"        # Use maven/gradle hooks
    # ... etc
```

### 2. Install Pre-commit Hooks

**JavaScript (Husky + lint-staged)**:
```bash
npm install --save-dev husky lint-staged
npx husky init
```

`.husky/pre-commit`:
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run tests for staged files
npx lint-staged

# Check coverage delta
npm run test:coverage -- --changedSince=HEAD~1
```

**Python (pre-commit)**:
```bash
pip install pre-commit
pre-commit install
```

`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: pytest --cov=src --cov-fail-under=80
        language: system
        types: [python]
        pass_filenames: false
```

### 3. Configure CI Coverage Gates

**GitHub Actions**:
```yaml
name: Test Coverage Gate
on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run tests with coverage
        run: npm test -- --coverage

      - name: Check coverage threshold
        run: |
          COVERAGE=$(jq '.total.lines.pct' coverage/coverage-summary.json)
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi

      - name: Comment coverage on PR
        uses: actions/github-script@v7
        with:
          script: |
            const coverage = require('./coverage/coverage-summary.json');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Coverage Report\n- Lines: ${coverage.total.lines.pct}%\n- Branches: ${coverage.total.branches.pct}%`
            });
```

### 4. Configure Test Presence Validation

Check that new/modified files have corresponding tests:

```python
def validate_test_presence(changed_files):
    """Ensure every source file has a test file"""
    missing_tests = []

    for src_file in changed_files:
        if is_source_file(src_file):
            test_file = get_test_file_path(src_file)
            if not exists(test_file):
                missing_tests.append(src_file)

    if missing_tests:
        print("ERROR: Missing tests for:")
        for f in missing_tests:
            print(f"  - {f}")
        return False
    return True
```

## Output Format

When reporting TDD enforcement setup:

```markdown
## TDD Enforcement Configured

### Pre-commit Hooks
- [x] Husky installed and initialized
- [x] Pre-commit hook: Run affected tests
- [x] Pre-commit hook: Check test presence for new files

### Coverage Gates
- Line coverage threshold: 80%
- Branch coverage threshold: 75%
- Critical path coverage: 100%

### CI Integration
- [x] GitHub Actions workflow created
- [x] Coverage gate: Fail PR if coverage < 80%
- [x] PR comment: Coverage report

### Files Created/Modified
- `.husky/pre-commit`
- `.github/workflows/test-coverage.yml`
- `package.json` (scripts updated)

### Next Steps
1. Run `npm test` to verify baseline coverage
2. Commit and push to test CI gates
3. Review coverage report on first PR
```

## Gradual Adoption for Brownfield

For existing projects without tests:

### Phase 1: Audit Mode (Week 1-2)
```yaml
enforcement: audit
# Log coverage but don't block
# Establish baseline
```

### Phase 2: New Code Only (Week 3-4)
```yaml
enforcement: gradual
coverage_delta: true  # Only check new code
threshold: 80
```

### Phase 3: Full Enforcement (Week 5+)
```yaml
enforcement: standard
threshold: 80
block_on_decrease: true
```

## Integration Points

- Works with `/setup-tdd` command
- Integrates with `mutation-test` skill for quality validation
- Feeds into `/flow-gate-check` for phase transitions
- Reports to Test Architect agent

## Related Skills

- `mutation-test` - Validate test quality beyond coverage
- `flaky-detect` - Identify unreliable tests
- `generate-factory` - Create test data infrastructure
- `test-sync` - Maintain test-code alignment

## Script Reference

### tdd_setup.py

Configure TDD enforcement for project:

```bash
# Standard enforcement (80% line, 75% branch)
python scripts/tdd_setup.py --level standard

# Custom thresholds
python scripts/tdd_setup.py --threshold 90 --branch-threshold 85

# Gradual adoption for brownfield projects
python scripts/tdd_setup.py --level gradual

# Preview without making changes
python scripts/tdd_setup.py --dry-run
```

Options:
- `--level`: Enforcement level (strict, standard, gradual, audit)
- `--threshold`: Line coverage threshold (default: 80)
- `--branch-threshold`: Branch coverage threshold (default: 75)
- `--dry-run`: Show what would be done without making changes
