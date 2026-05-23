---
name: technical-debt-detector
description: Identify and prioritize technical debt in Python codebases. Use when the user asks to find tech debt, analyze code quality, identify what needs refactoring, find security issues, check test coverage gaps, review dependencies, find TODOs/FIXMEs, or assess maintainability. Triggers on phrases like "find technical debt", "what's wrong with this codebase", "where should I focus refactoring", "audit this code", "find TODOs", "check for security issues", "analyze dependencies", or "what needs tests". Complements python-simplifier skill (use that for complexity and code smell analysis).
---

# Technical Debt Detector

Efficiently identify technical debt in large Python projects using scripts that output targeted file locations, minimizing token cost.

## Quick Start

```bash
# Full analysis - produces prioritized report
python scripts/analyze_all.py /path/to/project

# JSON output for programmatic use
python scripts/analyze_all.py /path/to/project --format json

# Run specific checks only
python scripts/analyze_all.py /path/to/project --only security testing
```

## Individual Analyzers

Run specific checks when focused analysis is needed:

| Script | Purpose | Key Outputs |
|--------|---------|-------------|
| `analyze_all.py` | Master analyzer - runs all checks | Prioritized report with fix sketches |
| `find_deferred_work.py` | TODO/FIXME/HACK/XXX markers | Location + message + severity |
| `find_security_issues.py` | Security vulnerabilities (uses bandit) | CVEs, hardcoded secrets, unsafe patterns |
| `analyze_test_coverage.py` | Missing tests, coverage gaps | Untested modules, empty tests |
| `find_maintainability_issues.py` | Docstrings, type hints, naming | Missing docs, bad names, long functions |
| `check_dependencies.py` | Outdated packages, vulnerabilities | Versions, CVEs, unpinned deps |

### Usage Examples

```bash
# Find all deferred work
python scripts/find_deferred_work.py /path/to/project
python scripts/find_deferred_work.py . --severity high  # Only FIXME/BUG/HACK/XXX

# Security scan
python scripts/find_security_issues.py /path/to/project

# Test coverage analysis
python scripts/analyze_test_coverage.py /path/to/project
python scripts/analyze_test_coverage.py . --run-coverage  # Include pytest-cov

# Maintainability check
python scripts/find_maintainability_issues.py /path/to/project
python scripts/find_maintainability_issues.py . --check docstrings  # Focus on docs

# Dependency health
python scripts/check_dependencies.py /path/to/project
python scripts/check_dependencies.py . --only vulnerabilities  # Just CVEs
```

## Workflow

1. **Run full analysis**: `python scripts/analyze_all.py /path/to/project`
2. **Review prioritized report**: High → Medium → Low severity
3. **For each high-priority item**:
   - Navigate to file:line
   - Apply fix sketch from report
   - See `references/fix_patterns.md` for detailed patterns
4. **For complexity/code smells**: Use python-simplifier skill

## Output Format

All scripts support `--format json` for integration with other tools:

```bash
python scripts/analyze_all.py . --format json | jq '.[] | select(.severity == "high")'
```

## Dependencies

Required (install if not present):
- `bandit` - Security analysis: `pip install bandit`
- `pip-audit` - Vulnerability scanning: `pip install pip-audit`

Optional (for deeper analysis):
- `pytest-cov` - Coverage analysis: `pip install pytest-cov`

## Severity Levels

- **High** 🔴: Fix immediately (security vulnerabilities, FIXME/BUG markers, critical gaps)
- **Medium** 🟡: Fix soon (TODOs, missing docstrings, outdated dependencies)
- **Low** 🔵: Fix when convenient (missing type hints, NOTEs, minor style issues)

## Relationship to python-simplifier

This skill focuses on **deferred work, security, testing, maintainability, and dependencies**.

For **complexity and code smells** (cyclomatic complexity, duplication, coupling, dead code, over-engineering), use the `python-simplifier` skill.
