---
name: dependency-resolver
version: 1.0.0
description: Automated dependency conflict detection and resolution. Detects local vs CI environment mismatches, compares versions, and generates pinning recommendations. Run as pre-push check to catch issues early.
auto_activates:
  - "dependency conflict"
  - "version mismatch"
  - "CI failing on linting"
  - "works locally but fails in CI"
  - "pre-push validation"
priority_score: 42.0
evaluation_criteria:
  frequency: HIGH
  impact: HIGH
  complexity: LOW
  reusability: HIGH
  philosophy_alignment: HIGH
  uniqueness: HIGH
---

# Dependency Resolver Skill

## Purpose

This skill detects and resolves local vs CI environment mismatches BEFORE push, preventing the 20-45 minute debug cycles documented in DISCOVERIES.md ("CI Failure Resolution Process Analysis" entry).

The skill addresses a critical gap: existing tools (ci-diagnostic-workflow, pre-commit-diagnostic) fix issues AFTER they occur. This skill catches mismatches BEFORE push.

## Problem Statement

From DISCOVERIES.md analysis:

- Environment mismatches (Local Python 3.12 vs CI Python 3.11) cause 20-25 min investigation overhead
- Version drift (local ruff 0.12.7 vs CI ruff 0.13.0) causes silent failures
- 45-minute complex debugging sessions traced to dependency conflicts
- No automated pre-push environment comparison exists

## Execution Instructions

When activated, execute these steps autonomously:

### Step 1: Collect Local Environment

```bash
# Python version
python --version

# Installed tool versions
pip show ruff black pyright mypy 2>/dev/null | grep -E "^(Name|Version):"

# Pre-commit hook versions (if available)
cat .pre-commit-config.yaml 2>/dev/null | grep -E "rev:|repo:"
```

### Step 2: Read CI Configuration

```
Read(file_path=".github/workflows/ci.yml")
Read(file_path="pyproject.toml")
Read(file_path=".pre-commit-config.yaml")
```

Extract:

- CI Python version (look for `python-version:`)
- Required tool versions from pyproject.toml
- Pre-commit hook versions from .pre-commit-config.yaml

### Step 3: Compare Environments

Build comparison table:

| Component | Local   | CI     | Status   |
| --------- | ------- | ------ | -------- |
| Python    | 3.12.10 | 3.11   | MISMATCH |
| ruff      | 0.12.7  | 0.13.0 | MISMATCH |
| black     | 24.3.0  | 24.3.0 | OK       |

### Step 4: Generate Recommendations

For each mismatch, provide actionable fix:

**Python Version Mismatch:**

```bash
# Option A: Use pyenv to match CI version
pyenv install 3.11
pyenv local 3.11

# Option B: Update CI to match local (if local is intentional)
# Edit .github/workflows/ci.yml line 33
```

**Tool Version Mismatch:**

```bash
# Pin versions in pyproject.toml
pip install ruff==0.13.0

# Or update pre-commit hooks
pre-commit autoupdate
```

### Step 5: Auto-Fix (When Requested)

If user requests auto-fix:

1. Update .pre-commit-config.yaml with latest versions
2. Run `pre-commit autoupdate`
3. Regenerate requirements.txt if applicable
4. Stage changes for commit

## Integration Points

### With fix-agent

Integrates with fix-agent templates for:

- Import/dependency fixes (Template 1)
- Configuration fixes (Template 2)
- CI/CD fixes (Template 4)

### With pre-commit-diagnostic

Hand-off when pre-commit failures detected after version sync.

### With ci-diagnostic-workflow

Hand-off for post-push CI failures not caught by pre-push validation.

## Common Mismatch Patterns

### Pattern 1: Python Minor Version Drift

**Symptoms:**

- Type errors only in CI
- Import errors with newer syntax
- f-string issues

**Fix:**

```bash
# Check CI Python version
grep -r "python-version" .github/workflows/

# Match locally or update CI
```

### Pattern 2: Linter Version Drift

**Symptoms:**

- "Works locally but CI fails on linting"
- New rules in CI not enforced locally
- Formatting differences

**Fix:**

```bash
# Sync pre-commit hooks to latest
pre-commit autoupdate

# Or pin specific version
pip install ruff==<ci-version>
```

### Pattern 3: Missing Dependencies

**Symptoms:**

- ModuleNotFoundError in CI
- Optional dependencies not installed

**Fix:**

```bash
# Install all optional dependencies
pip install -e ".[dev]"

# Ensure requirements.txt is up to date
pip freeze > requirements.txt
```

## Output Format

````markdown
## Dependency Resolver Report

### Environment Comparison

| Component | Local   | CI      | Status   |
| --------- | ------- | ------- | -------- |
| Python    | 3.12.10 | 3.11    | MISMATCH |
| ruff      | 0.12.7  | 0.13.0  | MISMATCH |
| pyright   | 1.1.350 | 1.1.350 | OK       |

### Mismatches Found: 2

### Recommendations

1. **Python Version** (CRITICAL)
   - Local: 3.12.10, CI: 3.11
   - Action: Consider using pyenv to test with CI version before push
   - Risk: Type syntax differences may cause failures

2. **ruff Version** (WARNING)
   - Local: 0.12.7, CI: 0.13.0
   - Action: Run `pip install ruff==0.13.0` or `pre-commit autoupdate`
   - Risk: New rules may flag previously passing code

### Quick Fix Commands

```bash
# Sync ruff version
pip install ruff==0.13.0

# Update all pre-commit hooks
pre-commit autoupdate

# Re-run pre-commit to validate
pre-commit run --all-files
```

### Status: ACTION REQUIRED

Push may fail due to environment mismatches.
Run recommended fixes before pushing.
````

## When to Use This Skill

**Trigger Signs:**

- "CI is failing but it works locally"
- "Linting passes here but not in CI"
- Before pushing after long development session
- After updating local Python or tools
- When onboarding to new project

**Not Needed When:**

- CI already passing consistently
- Environment just synced
- Only editing documentation

## Related Resources

- **DISCOVERIES.md**: CI Failure Resolution Process Analysis (lines 836-914)
- **fix-agent.md**: Templates for import/config/CI fixes
- **ci-diagnostic-workflow.md**: Post-push CI failure resolution
- **pre-commit-diagnostic.md**: Pre-commit hook failures
- **.github/workflows/ci.yml**: CI configuration source of truth

## Philosophy Alignment

### Ruthless Simplicity

- Procedural approach: Five clear steps, no unnecessary abstraction
- Direct shell commands: Users can copy-paste recommendations
- Focused scope: Only detects environment mismatches, delegates fixes to existing agents

### Zero-BS Implementation

- Actionable output: Every recommendation includes exact commands
- No theoretical advice: Specific version numbers and file paths
- Pre-push prevention: Catches issues before wasted CI cycles

### Modular Design

- Clean hand-offs: Integrates with fix-agent, pre-commit-diagnostic, ci-diagnostic-workflow
- Single responsibility: Detection and comparison only; fixes delegated to specialized agents
- Regeneratable: Can be rebuilt from this specification
