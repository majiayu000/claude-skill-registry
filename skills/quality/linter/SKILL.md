---
name: golangci-lint
description: Initialize or update golangci-lint configuration for Go projects with comprehensive code quality checks, static analysis, and best practices enforcement
---

# golangci-lint Setup Skill

Configure professional-grade linting for Go projects with sensible defaults that balance code quality with pragmatic development.

## Overview

[golangci-lint](https://golangci-lint.run) is a fast, parallel linter aggregator for Go that runs 90+ linters simultaneously. It's the industry standard for Go code quality enforcement.

**Benefits:**
- **Speed**: Runs linters in parallel with caching (5x faster than individual linters)
- **Comprehensive**: 90+ linters covering code quality, bugs, performance, and style
- **Configurable**: Highly customizable via YAML configuration
- **CI/CD Ready**: Seamless integration with GitHub Actions, GitLab CI, and pre-commit hooks
- **Editor Integration**: Works with VS Code, GoLand, Vim, and Emacs

This skill provides a battle-tested configuration (in `assets/.golangci.yml`) optimized for golangci-lint v2.4.0+ that enables all linters by default while disabling overly strict or opinionated ones.

## Prerequisites

1. **Go installed**: Go 1.21+ recommended (`go version`)
2. **golangci-lint installed**: Version 2.4.0+
   - macOS: `brew install golangci-lint`
   - Other: `go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest`
   - Verify: `golangci-lint --version`
3. **Go module**: Project uses Go modules (`go.mod` exists)

## Instructions

### Step 1: Verify Project Setup

```bash
# Verify Go module
ls go.mod

# Check for existing config
ls -la .golangci.yml .golangci.yaml

# Verify installation (should be version >=2)
golangci-lint --version
```

### Step 2: Copy Configuration File

Copy the base configuration from assets:

```bash
# Copy template to project root
cp assets/.golangci.yml .golangci.yml
```

The asset configuration follows these principles:
- **Enable all by default**: Maximum coverage with `default: all`
- **Disable the noisy**: Removes linters that are too opinionated or project-specific
- **Pragmatic over perfect**: Balances quality with development velocity
- **Project-agnostic**: Works for most Go projects out of the box

### Step 3: Run Initial Lint Check

Test the configuration:

```bash
# Run linter on entire project
golangci-lint run ./...

# Verbose output to see active linters
golangci-lint run -v ./...

# Test specific linter
golangci-lint run --disable-all --enable=govet ./...
```

### Step 6: Integrate with CI/CD

#### GitHub Actions

Already configured if using the `github-workflows` skill. Otherwise:

```yaml
- name: golangci-lint
  uses: golangci/golangci-lint-action@v6
  with:
    version: v2.4.0
    args: --timeout=5m
```

#### GitLab CI

```yaml
lint:
  stage: test
  image: golangci/golangci-lint:v2.4.0
  script:
    - golangci-lint run -v ./...
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

#### Taskfile Integration

```yaml
version: '3'

tasks:
  lint:
    desc: Run golangci-lint
    cmds:
      - golangci-lint run --timeout=5m ./...

  lint:fix:
    desc: Run with auto-fix
    cmds:
      - golangci-lint run --fix --timeout=5m ./...
```

#### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/golangci/golangci-lint
    rev: v2.4.0
    hooks:
      - id: golangci-lint
        args: [--timeout=5m]
```

### Step 7: Document in README

Add to your project's README.md:

```markdown
## Code Quality

This project uses [golangci-lint](https://golangci-lint.run) for code quality enforcement.

**⚠️ All linting issues MUST be fixed before pushing commits.**

### Running the Linter

```bash
# Check for issues
golangci-lint run ./...

# Auto-fix where possible
golangci-lint run --fix ./...
```

### Pre-commit Checklist

1. ✅ Run `golangci-lint run ./...`
2. ✅ Fix all reported issues
3. ✅ Ensure tests pass: `go test ./...`
4. ✅ Commit and push

CI automatically checks all PRs. PRs with linting errors will be blocked.
```

### Step 8: Configure Editor Integration

#### VS Code

Install [Go extension](https://marketplace.visualstudio.com/items?itemName=golang.go) and add to `settings.json`:

```json
{
  "go.lintTool": "golangci-lint",
  "go.lintFlags": ["--fast"],
  "go.lintOnSave": "workspace"
}
```

#### GoLand/IntelliJ IDEA

1. Settings → Tools → File Watchers → Add (+)
2. Select "golangci-lint"
3. Configure: `golangci-lint run $FileDir$`

#### Vim/Neovim

With `ale` plugin:
```vim
let g:ale_linters = {'go': ['golangci-lint']}
let g:ale_go_golangci_lint_options = '--fast'
```

## Additional Resources

- **Official documentation**: https://golangci-lint.run
- **Configuration reference**: https://golangci-lint.run/usage/configuration/
- **Linters list**: https://golangci-lint.run/usage/linters/
- **GitHub repository**: https://github.com/golangci/golangci-lint
- **Editor integrations**: https://golangci-lint.run/usage/integrations/

## Expected Output

After using this skill, your project will have:

- Professional `.golangci.yml` configuration with 90+ linters
- Balanced settings (strict but pragmatic)
- CI/CD integration ready
- Editor integration support
- Fast, cached linting
- Automated code quality enforcement

Your Go code will meet professional quality standards with comprehensive checks for bugs, security issues, performance problems, and best practices.
