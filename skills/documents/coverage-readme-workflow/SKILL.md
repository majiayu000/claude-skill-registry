---
name: coverage-readme-workflow
description: Ensure test coverage percentage is displayed in README.md for Next.js and Python projects following industry standards
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: test-coverage-documentation
---

## What I do

I implement a complete test coverage documentation workflow that ensures coverage percentages are displayed in README.md files:

1. **Detect Project Type**: Identify whether the project is Next.js (JavaScript/TypeScript) or Python
2. **Run Tests with Coverage**: Execute test suite with coverage collection for the detected framework
3. **Parse Coverage Output**: Extract coverage percentage from test output (lines, statements, branches, functions)
4. **Generate Coverage Badge**: Create or update coverage badge in industry-standard format (Shields.io badge)
5. **Update README.md**: Add or update coverage badge and percentage display in README.md following industry best practices
6. **Handle Edge Cases**: Deal with missing coverage configuration, zero coverage, or coverage threshold violations

## When to use me

Use this workflow when:
- You're creating a new Next.js application or Python project
- You've just added tests to an existing project
- You want to ensure test coverage is visible in project documentation
- You're following industry standard practices for displaying code quality metrics
- You need to update coverage percentage after adding new features
- You're preparing for a code review or PR submission
- You want to track coverage trends over time

**Integration**: This skill is typically used alongside:
- `test-generator-framework`: After generating tests
- `nextjs-unit-test-creator`: After generating Next.js tests
- `python-pytest-creator`: After generating Python tests
- `nextjs-pr-workflow`: Before creating a PR
- `pr-creation-workflow`: Before creating a PR

## Prerequisites

- Next.js project with `package.json` OR Python project with `pyproject.toml`/`requirements.txt`
- Test framework installed (Jest/Vitest for Next.js, pytest for Python)
- Coverage tools available (built-in to Jest/Vitest, pytest-cov for pytest)
- README.md file exists in project root
- Write permissions to update README.md
- Tests must pass before coverage display

Note: If coverage tools are not installed, this skill will guide you through installation.

## Steps

### Step 1: Detect Project Type

Determine project type by checking configuration files:

```bash
# Check for Next.js project
if [ -f "package.json" ]; then
  if grep -q '"next"' package.json; then
    PROJECT_TYPE="nextjs"
  else
    PROJECT_TYPE="nodejs"
  fi
fi

# Check for Python project
if [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
  PROJECT_TYPE="python"
fi

echo "Detected project type: $PROJECT_TYPE"
```

**Project Types:**
- `nextjs`: Next.js application (React framework)
- `nodejs`: JavaScript/TypeScript project without Next.js
- `python`: Python project

### Step 2: Detect Test Framework and Coverage Tool

#### Next.js Projects:

```bash
# Check package.json for test dependencies
if grep -q '"vitest"' package.json; then
  TEST_FRAMEWORK="vitest"
  COVERAGE_CMD="npm run test -- --coverage"
elif grep -q '"jest"' package.json; then
  TEST_FRAMEWORK="jest"
  COVERAGE_CMD="npm run test -- --coverage"
else
  # Check for test scripts
  if grep -q '"test:coverage"' package.json; then
    COVERAGE_CMD="npm run test:coverage"
  else
    echo "⚠️  No coverage command found in package.json"
    echo "Please add coverage script to package.json"
  fi
fi
```

#### Python Projects:

```bash
# Check if pytest-cov is installed
if grep -q '"pytest-cov"' pyproject.toml 2>/dev/null || grep -q "pytest-cov" requirements.txt 2>/dev/null; then
  TEST_FRAMEWORK="pytest"
  COVERAGE_CMD="poetry run pytest --cov=. --cov-report=term 2>/dev/null || pytest --cov=. --cov-report=term"
else
  echo "⚠️  pytest-cov not installed"
  echo "Install with: pip install pytest-cov"
  echo "Or with Poetry: poetry add --group dev pytest-cov"
fi
```

### Step 3: Run Tests with Coverage

#### Next.js (Jest/Vitest):

```bash
# Run coverage
echo "Running coverage for Next.js project..."
$COVERAGE_CMD 2>&1 | tee /tmp/coverage_output.txt

# Parse coverage output
COVERAGE_PERCENT=$(grep -oP '\d+(?=%)' /tmp/coverage_output.txt | head -1)
LINES_COV=$(grep -oP 'Lines\s*:\s*\K\d+(?=%)' /tmp/coverage_output.txt | head -1)
STATEMENTS_COV=$(grep -oP 'Statements\s*:\s*\K\d+(?=%)' /tmp/coverage_output.txt | head -1)
BRANCHES_COV=$(grep -oP 'Branches\s*:\s*\K\d+(?=%)' /tmp/coverage_output.txt | head -1)
FUNCTIONS_COV=$(grep -oP 'Functions\s*:\s*\K\d+(?=%)' /tmp/coverage_output.txt | head -1)

echo "Coverage Results:"
echo "  Total: ${COVERAGE_PERCENT}%"
echo "  Lines: ${LINES_COV}%"
echo "  Statements: ${STATEMENTS_COV}%"
echo "  Branches: ${BRANCHES_COV}%"
echo "  Functions: ${FUNCTIONS_COV}%"
```

#### Python (pytest-cov):

```bash
# Run coverage
echo "Running coverage for Python project..."
$COVERAGE_CMD 2>&1 | tee /tmp/coverage_output.txt

# Parse coverage output
COVERAGE_PERCENT=$(grep -oP '\d+(?=%)' /tmp/coverage_output.txt | head -1)
LINES_COV=$(grep -oP 'Lines\s*:\s*\K\d+(?=%)' /tmp/coverage_output.txt | head -1)
BRANCHES_COV=$(grep -oP 'Branches\s*:\s*\K\d+(?=%)' /tmp/coverage_output.txt | head -1)

echo "Coverage Results:"
echo "  Total: ${COVERAGE_PERCENT}%"
echo "  Lines: ${LINES_COV}%"
echo "  Branches: ${BRANCHES_COV}%"
```

### Step 4: Generate Coverage Badge

Create coverage badge in industry-standard Shields.io format:

```bash
# Badge URL format
BADGE_URL="https://img.shields.io/badge/coverage-${COVERAGE_PERCENT}%25-${BADGE_COLOR}.svg"

# Determine badge color based on coverage percentage
if [ "${COVERAGE_PERCENT}" -ge 80 ]; then
  BADGE_COLOR="brightgreen"
elif [ "${COVERAGE_PERCENT}" -ge 60 ]; then
  BADGE_COLOR="yellow"
elif [ "${COVERAGE_PERCENT}" -ge 40 ]; then
  BADGE_COLOR="orange"
else
  BADGE_COLOR="red"
fi

# Generate badge markdown
COVERAGE_BADGE="![Coverage](${BADGE_URL})"
echo "Coverage badge: ${COVERAGE_BADGE}"
```

**Badge Color Scheme (Industry Standard):**
- **brightgreen** (>= 80%): Excellent coverage
- **yellow** (60-79%): Good coverage, room for improvement
- **orange** (40-59%): Moderate coverage, needs attention
- **red** (< 40%): Poor coverage, requires immediate action

### Step 5: Update README.md

#### Check for Existing Coverage Badge:

```bash
if grep -q "coverage" README.md; then
  EXISTING_COVERAGE=true
  echo "Found existing coverage badge in README.md"
else
  EXISTING_COVERAGE=false
  echo "No existing coverage badge found"
fi
```

#### Update README.md Based on Project Type:

**For Next.js Projects:**

```bash
if [ "$EXISTING_COVERAGE" = "true" ]; then
  # Update existing coverage badge
  sed -i "s|!\[Coverage\](.*)|${COVERAGE_BADGE}|" README.md
else
  # Add new coverage badge section
  # Find the badges line or project title
  if grep -q "^\[!\[" README.md; then
    # Insert after existing badges
    sed -i "/^\[!\[.*\](.*)\]/a ${COVERAGE_BADGE}" README.md
  else
    # Insert after project title
    sed -i "1,/^# /s|^# \(.*\)|# \1\n\n${COVERAGE_BADGE}|" README.md
  fi
fi
```

**For Python Projects:**

```bash
if [ "$EXISTING_COVERAGE" = "true" ]; then
  # Update existing coverage badge
  sed -i "s|!\[Coverage\](.*)|${COVERAGE_BADGE}|" README.md
else
  # Add new coverage badge section
  if grep -q "^\[!\[" README.md; then
    # Insert after existing badges
    sed -i "/^\[!\[.*\](.*)\]/a ${COVERAGE_BADGE}" README.md
  else
    # Insert after project title
    sed -i "1,/^# /s|^# \(.*\)|# \1\n\n${COVERAGE_BADGE}|" README.md
  fi
fi
```

#### Add Coverage Section (If Not Exists):

```bash
# Add detailed coverage section to README
if ! grep -q "## Test Coverage" README.md; then
  # Find insertion point (after Badges or Description section)
  cat >> README.md << 'EOF'

## Test Coverage

[![Coverage](https://img.shields.io/badge/coverage-${COVERAGE_PERCENT}%25-${BADGE_COLOR}.svg)]

| Metric | Coverage |
|--------|----------|
| Lines | ${LINES_COV}% |
| Statements | ${STATEMENTS_COV}% |
| Branches | ${BRANCHES_COV}% |
| Functions | ${FUNCTIONS_COV}% |

**Total Coverage:** ${COVERAGE_PERCENT}%

To run tests with coverage:
```bash
${COVERAGE_CMD}
```

EOF
fi
```

### Step 6: Verify README.md Update

```bash
echo "✅ README.md updated successfully!"
echo ""
echo "Coverage badge added:"
grep -o '\[!\[Coverage\].*svg\)' README.md
echo ""
echo "To view README.md:"
echo "  cat README.md"
echo ""
echo "To commit changes:"
echo "  git add README.md"
echo "  git commit -m 'docs: update coverage badge to ${COVERAGE_PERCENT}%'"
```

### Step 7: Display Summary

```bash
echo "==================================================================="
echo "Coverage Documentation Complete!"
echo "==================================================================="
echo ""
echo "Project Type: $PROJECT_TYPE"
echo "Test Framework: $TEST_FRAMEWORK"
echo ""
echo "Coverage Results:"
echo "  Overall: ${COVERAGE_PERCENT}%"
echo "  Lines: ${LINES_COV}%"
if [ -n "${STATEMENTS_COV}" ]; then
  echo "  Statements: ${STATEMENTS_COV}%"
fi
if [ -n "${BRANCHES_COV}" ]; then
  echo "  Branches: ${BRANCHES_COV}%"
fi
if [ -n "${FUNCTIONS_COV}" ]; then
  echo "  Functions: ${FUNCTIONS_COV}%"
fi
echo ""
echo "Badge Color: ${BADGE_COLOR}"
echo "Badge URL: ${BADGE_URL}"
echo ""
echo "README.md has been updated with coverage badge."
echo "==================================================================="
```

## Coverage Badge Templates

### Basic Badge (Minimal):

```markdown
![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)
```

### Comprehensive Badge Section:

```markdown
## Badges

[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)](https://github.com/username/repo/actions/workflows/test.yml)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/username/repo/actions/workflows/test.yml)
```

### Detailed Coverage Table:

```markdown
## Test Coverage

| Metric | Coverage | Badge |
|--------|----------|--------|
| Overall | 85% | ![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg) |
| Lines | 87% | ![Lines](https://img.shields.io/badge/lines-87%25-brightgreen.svg) |
| Branches | 82% | ![Branches](https://img.shields.io/badge/branches-82%25-yellow.svg) |
| Functions | 88% | ![Functions](https://img.shields.io/badge/functions-88%25-brightgreen.svg) |

**To run tests with coverage:**
```bash
npm run test -- --coverage
```
```

## Coverage Thresholds (Industry Standards)

| Coverage Range | Quality Level | Badge Color | Action Required |
|----------------|--------------|-------------|----------------|
| 90-100% | Excellent | brightgreen | Maintain |
| 80-89% | Good | brightgreen | Monitor |
| 70-79% | Acceptable | yellow | Improve |
| 60-69% | Fair | orange | Improve |
| 0-59% | Poor | red | Improve immediately |

## Best Practices

- **Minimum Coverage**: Aim for at least 80% coverage for production code
- **Badge Placement**: Place coverage badge prominently at the top of README.md
- **Automatic Updates**: Set up CI/CD pipeline to update badge automatically
- **Multiple Metrics**: Display overall coverage and breakdown (lines, branches, functions)
- **Trend Tracking**: Consider showing coverage trends over time
- **Threshold Enforcement**: Configure coverage thresholds in test configuration
- **False Positives**: Exclude test files and non-critical code from coverage
- **Documentation**: Explain how to run tests with coverage in README.md

## Next.js-Specific Best Practices

### Jest Configuration:

```javascript
// jest.config.js
module.exports = {
  collectCoverageFrom: [
    'components/**/*.{js,jsx,ts,tsx}',
    'app/**/*.{js,jsx,ts,tsx}',
    'lib/**/*.{js,jsx,ts,tsx}',
    '!**/*.d.ts',
    '!**/node_modules/**',
    '!**/.next/**',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
}
```

### Vitest Configuration:

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        '.next/',
        '**/*.d.ts',
        '**/*.config.*',
      ],
      threshold: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
})
```

## Python-Specific Best Practices

### Pytest Configuration:

```ini
# .coveragerc
[run]
omit =
    tests/*
    */tests/*
    */__init__.py
    */migrations/*
    venv/*
    .venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
```

### Pytest Configuration with Thresholds:

```ini
# pytest.ini
[pytest]
addopts = --cov=. --cov-report=term-missing --cov-fail-under=80
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "--cov=. --cov-report=term-missing --cov-fail-under=80"

[tool.coverage.run]
omit = [
    "tests/*",
    "*/tests/*",
    "*/__init__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

## Common Issues

### Coverage Not Detected

**Issue**: Coverage percentage not extracted from test output

**Solution**:
```bash
# Check coverage output manually
npm run test -- --coverage
# or
pytest --cov=. --cov-report=term

# Verify coverage output format
# Jest/Vitest: "Coverage summary: 85%"
# pytest: "TOTAL 85%"
```

### Badge Not Updating

**Issue**: README.md badge shows old coverage percentage

**Solution**:
```bash
# Remove existing coverage badge
sed -i '/!\[Coverage\]/d' README.md

# Re-run coverage workflow
# This will re-add the badge with updated percentage
```

### Coverage Command Not Found

**Issue**: `npm run test -- --coverage` fails

**Solution**:

**For Next.js with Jest**:
```bash
# Add coverage script to package.json
jq '.scripts["test:coverage"] = "jest --coverage"' package.json > tmp.json && mv tmp.json package.json

# Or add flag to existing test script
jq '.scripts.test += " --coverage"' package.json > tmp.json && mv tmp.json package.json
```

**For Next.js with Vitest**:
```json
{
  "scripts": {
    "test:coverage": "vitest --coverage"
  }
}
```

**For Python with pytest**:
```bash
# Install pytest-cov
pip install pytest-cov

# Or with Poetry
poetry add --group dev pytest-cov
```

### README.md Not Found

**Issue**: README.md file doesn't exist

**Solution**:
```bash
# Create README.md
cat > README.md << 'EOF'
# Project Name

Brief description of the project.

EOF

# Now run coverage workflow to add badge
```

### Coverage Too Low

**Issue**: Coverage badge shows red color (below 40%)

**Solution**:
- Identify uncovered code: `npm run test -- --coverage --coverageReporters=json`
- Review coverage report in `coverage/coverage-final.json`
- Add tests for uncovered code
- Re-run coverage workflow
- Commit updated README.md with improved badge

### Coverage Exclusions Not Working

**Issue**: Test files or non-critical code included in coverage

**Solution**:

**For Jest/Vitest**:
```javascript
// Update jest.config.js or vitest.config.ts
collectCoverageFrom: [
  'src/**/*.{js,jsx,ts,tsx}',
  '!src/**/*.test.{js,jsx,ts,tsx}',
  '!src/**/*.spec.{js,jsx,ts,tsx}',
  '!src/types/**',
]
```

**For pytest**:
```ini
# Update .coveragerc or pyproject.toml
[run]
omit =
    tests/*
    */tests/*
    test_*.py
    *_test.py
```

## Troubleshooting Checklist

Before running coverage workflow:
- [ ] Project type detected (Next.js or Python)
- [ ] Test framework installed (Jest/Vitest or pytest)
- [ ] Coverage tool available (built-in or pytest-cov)
- [ ] Tests pass without coverage
- [ ] README.md exists in project root
- [ ] Write permissions to update README.md

After running coverage workflow:
- [ ] Coverage badge added to README.md
- [ ] Badge shows correct percentage
- [ ] Badge color reflects coverage level
- [ ] Coverage breakdown displayed (if applicable)
- [ ] Test command documented in README.md
- [ ] README.md updated in git

## Integration with Other Skills

### After Test Generation:

1. `test-generator-framework` → `coverage-readme-workflow`
2. `nextjs-unit-test-creator` → `coverage-readme-workflow`
3. `python-pytest-creator` → `coverage-readme-workflow`

### Before PR Creation:

1. `coverage-readme-workflow` → `pr-creation-workflow`
2. `coverage-readme-workflow` → `nextjs-pr-workflow`

### Complete Workflow Example:

```bash
# 1. Generate tests (example: Next.js)
opencode --agent nextjs-unit-test-creator "generate tests for new components"

# 2. Run tests to verify they pass
npm run test

# 3. Run coverage and update README
opencode --agent coverage-readme-workflow "update coverage badge"

# 4. Commit changes
git add .
git commit -m "feat: add tests and coverage badge (85%)"

# 5. Create PR
opencode --agent nextjs-pr-workflow "create PR with test coverage"
```

## Related Skills

- `nextjs-standard-setup`: For creating standardized Next.js 16 applications with proper component architecture
- `test-generator-framework`: Core test generation framework
- `nextjs-unit-test-creator`: Next.js test generation
- `python-pytest-creator`: Python test generation
- `pr-creation-workflow`: PR creation with quality checks
- `nextjs-pr-workflow`: Next.js PR workflow
- `linting-workflow`: Code quality checks before testing
