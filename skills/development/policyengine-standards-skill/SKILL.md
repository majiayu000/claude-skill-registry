---
name: policyengine-standards
description: PolicyEngine coding standards, formatters, CI requirements, and development best practices
---

# PolicyEngine Standards Skill

Use this skill to ensure code meets PolicyEngine's development standards and passes CI checks.

## When to Use This Skill

- Before committing code to any PolicyEngine repository
- When CI checks fail with linting/formatting errors
- Setting up a new PolicyEngine repository
- Reviewing PRs for standard compliance
- When AI tools generate code that needs standardization

## Critical Requirements

### Python Version
⚠️ **MUST USE Python 3.13** - Do NOT downgrade to older versions
- Check version: `python --version`
- Use `pyproject.toml` to specify version requirements

### Command Execution
⚠️ **ALWAYS use `uv run` for Python commands** - Never use bare `python` or `pytest`
- ✅ Correct: `uv run python script.py`, `uv run pytest tests/`
- ❌ Wrong: `python script.py`, `pytest tests/`
- This ensures correct virtual environment and dependencies

### Documentation (Python Projects)
⚠️ **MUST USE Jupyter Book 2.0 (MyST-NB)** - NOT Jupyter Book 1.x
- Build docs: `myst build docs` (NOT `jb build`)
- Use MyST markdown syntax

## Before Committing - Checklist

1. **Write tests first** (TDD - see below)
2. **Format code**: `make format` or language-specific formatter
3. **Run tests**: `make test` to ensure all tests pass
4. **Check linting**: Ensure no linting errors
5. **Use config files**: Prefer config files over environment variables
6. **Reference issues**: Include "Fixes #123" in commit message

## Creating Pull Requests

### The CI Waiting Problem

**Common failure pattern:**
```
User: "Create a PR and mark it ready when CI passes"
Claude: "I've created the PR as draft. CI will take a while, I'll check back later..."
[Chat ends - Claude never checks back]
Result: PR stays in draft, user has to manually check CI and mark ready
```

### Solution: Use /create-pr Command

**When creating PRs, use the /create-pr command:**

```bash
/create-pr
```

**This command:**
- ✅ Creates PR as draft
- ✅ Actually waits for CI (polls every 15 seconds)
- ✅ Marks ready when CI passes
- ✅ Reports failures with details
- ✅ Handles timeouts gracefully

**Why this works:**
The command contains explicit polling logic that Claude executes, so it actually waits instead of giving up.

### If /create-pr is Not Available

**If the command isn't installed, implement the pattern directly:**

```bash
# 1. Create PR as draft
# CRITICAL: Use --repo flag to create PR in upstream repo from fork
gh pr create --repo PolicyEngine/policyengine-us --draft --title "Title" --body "Body"
PR_NUMBER=$(gh pr view --json number --jq '.number')

# 2. Wait for CI (ACTUALLY WAIT - don't give up!)
POLL_INTERVAL=15
ELAPSED=0

while true; do  # No timeout - wait as long as needed
  CHECKS=$(gh pr checks $PR_NUMBER --json status,conclusion)
  TOTAL=$(echo "$CHECKS" | jq '. | length')
  COMPLETED=$(echo "$CHECKS" | jq '[.[] | select(.status == "COMPLETED")] | length')

  echo "[$ELAPSED s] CI: $COMPLETED/$TOTAL completed"

  if [ "$COMPLETED" -eq "$TOTAL" ] && [ "$TOTAL" -gt 0 ]; then
    FAILED=$(echo "$CHECKS" | jq '[.[] | select(.conclusion == "FAILURE")] | length')
    if [ "$FAILED" -eq 0 ]; then
      echo "✅ All CI passed! Marking ready..."
      gh pr ready $PR_NUMBER
      break
    else
      echo "❌ CI failed. PR remains draft."
      gh pr checks $PR_NUMBER
      break
    fi
  fi

  sleep $POLL_INTERVAL
  ELAPSED=$((ELAPSED + POLL_INTERVAL))
done

# Important: No timeout! Population simulations can take 30+ minutes.
```

### DO NOT Say "I'll Check Back Later"

**❌ WRONG:**
```
"I've created the PR as draft. CI checks will take a few minutes.
I'll check back later once they complete."
```

**Why wrong:** You cannot check back later. The chat session ends.

**✅ CORRECT:**
```
"I've created the PR as draft. Now polling CI status every 15 seconds..."
[Actually polls using while loop]
"CI checks completed. All passed! Marking PR as ready for review."
```

### When to Create Draft vs Ready

**Always create as draft when:**
- CI checks are configured
- User asks to wait for CI
- Making automated changes
- Unsure if CI will pass

**Create as ready only when:**
- User explicitly requests ready PR
- No CI configured
- CI already verified locally

### PR Workflow Standards

**Standard flow:**
```bash
# 1. Ensure branch is pushed
git push -u origin feature-branch

# 2. Create PR as draft (use --repo for cross-fork PRs)
gh pr create --repo PolicyEngine/policyengine-us --draft --title "..." --body "..."

# 3. Wait for CI (use polling loop - see pattern above)

# 4. If CI passes:
gh pr ready $PR_NUMBER

# 5. If CI fails:
echo "CI failed. PR remains draft. Fix issues and push again."
```

## Test-Driven Development (TDD)

PolicyEngine follows Test-Driven Development practices across all repositories.

### TDD Workflow

**1. Write test first (RED):**
```python
# tests/test_new_feature.py
def test_california_eitc_calculation():
    """Test California EITC for family with 2 children earning $30,000."""
    situation = create_family(income=30000, num_children=2, state="CA")
    sim = Simulation(situation=situation)
    ca_eitc = sim.calculate("ca_eitc", 2024)[0]

    # Test fails initially (feature not implemented yet)
    assert ca_eitc == 3000, "CA EITC should be $3,000 for this household"
```

**2. Implement feature (GREEN):**
```python
# policyengine_us/variables/gov/states/ca/tax/income/credits/ca_eitc.py
class ca_eitc(Variable):
    value_type = float
    entity = TaxUnit
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        # Implementation to make test pass
        federal_eitc = tax_unit("eitc", period)
        return federal_eitc * parameters(period).gov.states.ca.tax.eitc.match
```

**3. Refactor (REFACTOR):**
```python
# Clean up, optimize, add documentation
# All while tests continue to pass
```

### TDD Benefits

**Why PolicyEngine uses TDD:**
- ✅ **Accuracy** - Tests verify implementation matches regulations
- ✅ **Documentation** - Tests show expected behavior
- ✅ **Regression prevention** - Changes don't break existing features
- ✅ **Confidence** - Safe to refactor
- ✅ **Isolation** - Multi-agent workflow (test-creator and rules-engineer work separately)

### TDD in Multi-Agent Workflow

**Country model development:**
1. **@document-collector** gathers regulations
2. **@test-creator** writes tests from regulations (isolated, no implementation access)
3. **@rules-engineer** implements from regulations (isolated, no test access)
4. Both work from same source → tests verify implementation accuracy

**See policyengine-core-skill and country-models agents for details.**

### Test Examples

**Python (pytest):**
```python
def test_ctc_for_two_children():
    """Test CTC calculation for married couple with 2 children."""
    situation = create_married_couple(
        income_1=75000,
        income_2=50000,
        num_children=2,
        child_ages=[5, 8]
    )

    sim = Simulation(situation=situation)
    ctc = sim.calculate("ctc", 2024)[0]

    assert ctc == 4000, "CTC should be $2,000 per child"
```

**React (Jest + RTL):**
```javascript
import { render, screen } from '@testing-library/react';
import TaxCalculator from './TaxCalculator';

test('displays calculated tax', () => {
  render(<TaxCalculator income={50000} />);

  // Test what user sees, not implementation
  expect(screen.getByText(/\$5,000/)).toBeInTheDocument();
});
```

### Test Organization

**Python:**
```
tests/
├── test_variables/
│   ├── test_income.py
│   ├── test_deductions.py
│   └── test_credits.py
├── test_parameters/
└── test_simulations/
```

**React:**
```
src/
├── components/
│   └── TaxCalculator/
│       ├── TaxCalculator.jsx
│       └── TaxCalculator.test.jsx
```

### Running Tests

**Python:**
```bash
# All tests
make test

# With uv
uv run pytest tests/ -v

# Specific test
uv run pytest tests/test_credits.py::test_ctc_for_two_children -v

# With coverage
uv run pytest tests/ --cov=policyengine_us --cov-report=html
```

**React:**
```bash
# All tests
make test

# Watch mode
npm test -- --watch

# Specific test
npm test -- TaxCalculator.test.jsx

# Coverage
npm test -- --coverage
```

### Test Quality Standards

**Good tests:**
- ✅ Test behavior, not implementation
- ✅ Clear, descriptive names
- ✅ Single assertion per test (when possible)
- ✅ Include documentation (docstrings)
- ✅ Based on official regulations with citations

**Bad tests:**
- ❌ Testing private methods
- ❌ Mocking everything
- ❌ No assertion messages
- ❌ Magic numbers without explanation

### Example: TDD for New Feature

```python
# Step 1: Write test (RED)
def test_new_york_empire_state_child_credit():
    """Test NY Empire State Child Credit for family with 1 child.

    Based on NY Tax Law Section 606(c-1).
    Family earning $50,000 with 1 child under 4 should receive $330.
    """
    situation = create_family(
        income=50000,
        num_children=1,
        child_ages=[2],
        state="NY"
    )

    sim = Simulation(situation=situation)
    credit = sim.calculate("ny_empire_state_child_credit", 2024)[0]

    assert credit == 330, "Should receive $330 for child under 4"

# Test fails - feature doesn't exist yet

# Step 2: Implement (GREEN)
# Create variable in policyengine_us/variables/gov/states/ny/...
# Test passes

# Step 3: Refactor
# Optimize, add documentation, maintain passing tests
```

## Python Standards

### Formatting
- **Formatter**: Black with 79-character line length
- **Command**: `make format` or `black . -l 79`
- **Check without changes**: `black . -l 79 --check`

```bash
# Format all Python files
make format

# Check if formatting is needed (CI-style)
black . -l 79 --check
```

### Code Style
```python
# Imports: Grouped and alphabetized
import os
import sys
from pathlib import Path  # stdlib

import numpy as np
import pandas as pd  # third-party

from policyengine_us import Simulation  # local

# Naming conventions
class TaxCalculator:  # CamelCase for classes
    pass

def calculate_income_tax(income):  # snake_case for functions
    annual_income = income * 12  # snake_case for variables
    return annual_income

# Type hints (recommended)
def calculate_tax(income: float, state: str) -> float:
    """Calculate state income tax.

    Args:
        income: Annual income in dollars
        state: Two-letter state code

    Returns:
        Tax liability in dollars
    """
    pass

# Error handling - catch specific exceptions
try:
    result = simulation.calculate("income_tax", 2024)
except KeyError as e:
    raise ValueError(f"Invalid variable name: {e}")
```

### Testing
```python
import pytest

def test_ctc_calculation():
    """Test Child Tax Credit calculation for family with 2 children."""
    situation = create_family(income=50000, num_children=2)
    sim = Simulation(situation=situation)
    ctc = sim.calculate("ctc", 2024)[0]

    assert ctc == 4000, "CTC should be $2000 per child"
```

**Run tests:**
```bash
# All tests
make test

# Or with uv
uv run pytest tests/ -v

# Specific test
uv run pytest tests/test_tax.py::test_ctc_calculation -v

# With coverage
uv run pytest tests/ --cov=policyengine_us --cov-report=html
```

## JavaScript/React Standards

### Formatting
- **Formatters**: Prettier + ESLint
- **Command**: `npm run lint -- --fix && npx prettier --write .`
- **CI Check**: `npm run lint -- --max-warnings=0`

```bash
# Format all files
make format

# Or manually
npm run lint -- --fix
npx prettier --write .

# Check if formatting is needed (CI-style)
npm run lint -- --max-warnings=0
```

### Code Style
```javascript
// Use functional components only (no class components)
import { useState, useEffect } from "react";

function TaxCalculator({ income, state }) {
  const [tax, setTax] = useState(0);

  useEffect(() => {
    // Calculate tax when inputs change
    calculateTax(income, state).then(setTax);
  }, [income, state]);

  return (
    <div>
      <p>Tax: ${tax.toLocaleString()}</p>
    </div>
  );
}

// File naming
// - Components: PascalCase.jsx (TaxCalculator.jsx)
// - Utilities: camelCase.js (formatCurrency.js)

// Environment config - use config file pattern
// src/config/environment.js
const config = {
  API_URL: process.env.NODE_ENV === 'production'
    ? 'https://api.policyengine.org'
    : 'http://localhost:5000'
};
export default config;
```

### React Component Size
- Keep components under 150 lines after formatting
- Extract complex logic into custom hooks
- Split large components into smaller ones

## Version Control Standards

### Changelog Management

**CRITICAL**: For PRs, ONLY modify `changelog_entry.yaml`. NEVER manually update `CHANGELOG.md` or `changelog.yaml`.

**Terminology Note:**
When someone says "add a changelog entry" or "needs a changelog entry" in PolicyEngine context, they mean:
- ✅ Create/update `changelog_entry.yaml` (the PR-level entry file)
- ❌ NOT editing `CHANGELOG.md` (the main changelog file)
- ❌ NOT editing `changelog.yaml` (the compiled changelog)

**Correct Workflow:**
1. Create `changelog_entry.yaml` at repository root:
   ```yaml
   - bump: patch  # or minor, major
     changes:
       added:
       - Description of new feature
       fixed:
       - Description of bug fix
       changed:
       - Description of change
   ```

2. Commit ONLY `changelog_entry.yaml` with your code changes

3. GitHub Actions automatically updates `CHANGELOG.md` and `changelog.yaml` on merge

**DO NOT:**
- ❌ Run `make changelog` manually during PR creation
- ❌ Commit `CHANGELOG.md` or `changelog.yaml` in your PR
- ❌ Modify main changelog files directly

### Git Workflow

1. **Create branches on PolicyEngine repos, NOT forks**
   - Forks cause CI failures due to missing secrets
   - Request write access if needed

2. **Branch naming**: `feature-name` or `fix-issue-123`

3. **Commit messages**:
   ```
   Add CTC reform analysis for CRFB report

   - Implement household-level calculations
   - Add state-by-state comparison
   - Create visualizations

   Fixes #123
   ```

4. **PR description**: Include "Fixes #123" to auto-close issues

### Common Git Pitfalls

**Never do these:**
- ❌ Force push to main/master
- ❌ Commit secrets or `.env` files
- ❌ Skip hooks with `--no-verify`
- ❌ Create versioned files (app_v2.py, component_new.jsx)

**Always do:**
- ✅ Fix original files in place
- ✅ Run formatters before pushing
- ✅ Reference issue numbers in commits
- ✅ Watch CI after filing PR

## Common AI Pitfalls

Since many PRs are AI-generated, watch for these common mistakes:

### 1. File Versioning
**❌ Wrong:**
```bash
# Creating new versions instead of fixing originals
app_new.py
app_v2.py
component_refactored.jsx
```

**✅ Correct:**
```bash
# Always modify the original file
app.py  # Fixed in place
```

### 2. Formatter Not Run
**❌ Wrong:** Committing without formatting (main cause of CI failures)

**✅ Correct:**
```bash
# Python
make format
black . -l 79

# React
npm run lint -- --fix
npx prettier --write .
```

### 3. Environment Variables
**❌ Wrong:**
```javascript
// React env vars without REACT_APP_ prefix
const API_URL = process.env.API_URL;  // Won't work!
```

**✅ Correct:**
```javascript
// Use config file pattern instead
import config from './config/environment';
const API_URL = config.API_URL;
```

### 4. Using Wrong Python Version
**❌ Wrong:** Downgrading to Python 3.10 or older

**✅ Correct:** Use Python 3.13 as specified in project requirements

### 5. Manual Changelog Updates
**❌ Wrong:** Running `make changelog` and committing `CHANGELOG.md`

**✅ Correct:** Only create `changelog_entry.yaml` in PR

## Repository Setup Patterns

### Python Package Structure
```
policyengine-package/
├── policyengine_package/
│   ├── __init__.py
│   ├── core/
│   ├── calculations/
│   └── utils/
├── tests/
│   ├── test_calculations.py
│   └── test_core.py
├── pyproject.toml
├── Makefile
├── CLAUDE.md
├── CHANGELOG.md
└── README.md
```

### React App Structure
```
policyengine-app/
├── src/
│   ├── components/
│   ├── pages/
│   ├── config/
│   │   └── environment.js
│   └── App.jsx
├── public/
├── package.json
├── .eslintrc.json
├── .prettierrc
└── README.md
```

## Makefile Commands

Standard commands across PolicyEngine repos:

```bash
make install    # Install dependencies
make test       # Run tests
make format     # Format code
make changelog  # Update changelog (automation only, not manual)
make debug      # Start dev server (apps)
make build      # Production build (apps)
```

## CI Stability

### Common CI Issues

**1. Fork PRs Fail**
- **Problem**: PRs from forks don't have access to repository secrets
- **Solution**: Create branches directly on PolicyEngine repos

**2. GitHub API Rate Limits**
- **Problem**: Smoke tests fail with 403 errors
- **Solution**: Re-run failed jobs (different runners have different limits)

**3. Linting Failures**
- **Problem**: Code not formatted before commit
- **Solution**: Always run `make format` before committing

**4. Test Failures in CI but Pass Locally**
- **Problem**: Missing `uv run` prefix
- **Solution**: Use `uv run pytest` instead of `pytest`

## Best Practices Checklist

### Code Quality
- [ ] Code formatted with Black (Python) or Prettier (JS)
- [ ] No linting errors
- [ ] All tests pass
- [ ] Type hints added (Python, where applicable)
- [ ] Docstrings for public functions/classes
- [ ] Error handling with specific exceptions

### Version Control
- [ ] Only `changelog_entry.yaml` created (not CHANGELOG.md)
- [ ] Commit message references issue number
- [ ] Branch created on PolicyEngine repo (not fork)
- [ ] No secrets or .env files committed
- [ ] Original files modified (no _v2 or _new files)

### Testing
- [ ] Tests written for new functionality
- [ ] Tests pass locally with `make test`
- [ ] Coverage maintained or improved
- [ ] Edge cases handled

### Documentation
- [ ] README updated if needed
- [ ] Code comments for complex logic
- [ ] API documentation updated if needed
- [ ] Examples provided for new features

## Quick Reference

### Format Commands by Language

**Python:**
```bash
make format                # Format code
black . -l 79 --check      # Check formatting
uv run pytest tests/ -v    # Run tests
```

**React:**
```bash
make format                              # Format code
npm run lint -- --max-warnings=0         # Check linting
npm test                                 # Run tests
```

### Pre-Commit Checklist
```bash
# 1. Format
make format

# 2. Test
make test

# 3. Check linting
# Python: black . -l 79 --check
# React: npm run lint -- --max-warnings=0

# 4. Stage and commit
git add .
git commit -m "Description

Fixes #123"

# 5. Push and watch CI
git push
```

## Resources

- **Main CLAUDE.md**: `/PolicyEngine/CLAUDE.md`
- **Python Style**: PEP 8, Black documentation
- **React Style**: Airbnb React/JSX Style Guide
- **Testing**: pytest documentation, Jest/RTL documentation
- **Writing Style**: See policyengine-writing-skill for blog posts, PR descriptions, and documentation

## Examples

See PolicyEngine repositories for examples of standard-compliant code:
- **policyengine-us**: Python package standards
- **policyengine-app**: React app standards
- **givecalc**: Streamlit app standards
- **crfb-tob-impacts**: Analysis repository standards
