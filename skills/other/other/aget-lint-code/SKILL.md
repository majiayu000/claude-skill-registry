---
name: aget-lint-code
description: Run code linting and formatting checks
archetype: developer
allowed-tools:
  - Bash
  - Read
  - Glob
---

# aget-lint-code

Run code linting and formatting checks on files or directories. Auto-detects linter configuration and reports issues by severity.

## Instructions

When this skill is invoked:

1. **Detect Linter Configuration**
   - Python: ruff, flake8, pylint (pyproject.toml, setup.cfg)
   - JavaScript: eslint (.eslintrc.*)
   - Go: golangci-lint (.golangci.yml)
   - YAML: yamllint

2. **Execute Linter**
   - Use project configuration
   - Target specified files or all
   - Capture output

3. **Process Results**
   - Categorize by severity (error, warning, info)
   - Extract file locations
   - Count issues

4. **Report Findings**
   - Summary by severity
   - Issue details with locations
   - Fix suggestions if available

## Execution Commands

```bash
# Python (ruff)
ruff check [path] --output-format=text

# Python (flake8)
flake8 [path]

# JavaScript (eslint)
npx eslint [path] --format stylish

# Go
golangci-lint run [path]

# YAML
yamllint [path]
```

## Output Format

```markdown
## Lint Results

### Summary

| Severity | Count |
|----------|-------|
| Errors | [N] |
| Warnings | [N] |
| Info | [N] |
| **Total** | [N] |

### Status: [CLEAN/ISSUES FOUND]

### Issues by File

#### [filename.py]

| Line | Severity | Rule | Message |
|------|----------|------|---------|
| [N] | Error | [E001] | [Description] |
| [N] | Warning | [W002] | [Description] |

### Auto-fixable

[N] issues can be auto-fixed with `--fix` flag.

### Recommended Actions

1. [Fix critical errors first]
2. [Address warnings]
```

## Constraints

- **C1**: NEVER apply auto-fixes without explicit --fix flag — lint is read-only by default
- **C2**: NEVER ignore configuration files — project configuration must be respected
- **C3**: NEVER fail silently when linter is misconfigured — configuration errors must be surfaced

## Related

- SKILL-023: aget-lint-code specification
- ONTOLOGY_developer.yaml: Code, Code_Change concepts
- CAP-DEV-002: Code Linting capability
