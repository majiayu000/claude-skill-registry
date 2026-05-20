---
name: validate-workflow
description: Validate GitHub Actions workflow files for syntax, best practices, and correctness. Use before committing workflow changes or when workflows fail.
mcp_fallback: none
category: ci
user-invocable: false
---

# CI Workflow Validation Skill

Validate GitHub Actions workflow files for correctness.

## When to Use

- Creating new workflow
- Modifying existing workflow
- Workflow syntax errors
- Before committing workflow changes

## Quick Reference

```bash
# List workflows
gh workflow list

# View workflow details
gh workflow view <workflow-name>

# Validate YAML
yamllint .github/workflows/*.yml

# Lint with actionlint
actionlint .github/workflows/*.yml
```

## Validation Methods

### 1. GitHub CLI

```bash
# View workflow
gh workflow view deploy.yml

# List all workflows
gh workflow list

# Get workflow metadata
gh api repos/owner/repo/actions/workflows
```

### 2. actionlint

```bash
pip install actionlint
actionlint .github/workflows/*.yml
```

### 3. yamllint

```bash
yamllint .github/workflows/*.yml
```

## Common Issues

| Issue | Example | Fix |
|-------|---------|-----|
| Syntax error | `on: [push pull_request]` | Add comma: `on: [push, pull_request]` |
| Invalid action version | `uses: actions/checkout@v99` | Use valid version: `@v4` |
| Missing required field | Job missing `runs-on` | Add `runs-on: ubuntu-latest` |
| Invalid context | `${{ job.status }}` in wrong place | Move to correct context |

## Workflow Checklist

- [ ] Valid YAML syntax
- [ ] `on` trigger configured correctly
- [ ] All jobs have `runs-on`
- [ ] All steps have `run` or `uses`
- [ ] Action versions are specific (not @main)
- [ ] All secrets/vars available
- [ ] Timeouts set appropriately
- [ ] Permissions configured correctly

## Best Practices

```yaml
name: Quality Check
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4      # Specific version
      - uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip

      - run: just pre-commit-all
```

## Validation Workflow

```bash
# 1. Edit workflow
vim .github/workflows/test.yml

# 2. Validate YAML
yamllint .github/workflows/test.yml

# 3. Lint with actionlint
actionlint .github/workflows/test.yml

# 4. Review in GitHub
gh workflow view test.yml

# 5. Commit if valid
git add .github/workflows/test.yml
git commit -m "ci: update workflow"
```

## Error Handling

| Error | Fix |
|-------|-----|
| "Invalid YAML" | Fix YAML syntax errors |
| "Unknown action" | Check action name and version |
| "Missing field" | Add required fields (run, uses, etc.) |
| "Invalid context" | Use correct context expression syntax |

## Configuration Files

- `.pre-commit-config.yaml` - Pre-commit hooks
- `.github/workflows/` - Workflow definitions
- `actionlint` config - Action linting rules

## References

- GitHub Actions docs: <https://docs.github.com/en/actions>
- Workflow syntax: <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
- Related skill: `fix-ci-failures` for debugging failures
