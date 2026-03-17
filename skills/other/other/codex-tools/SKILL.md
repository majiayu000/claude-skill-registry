---
name: codex-tools
description: Execute and manage Codex CLI tools including file operations, shell commands, web search, and automation patterns. Use for automated workflows, tool orchestration, and full automation with permission bypass.
---

# Codex Tools Execution

Comprehensive patterns for executing Codex CLI tools safely and with full automation.

**Last Updated**: December 2025 (GPT-5.2 Release)

## Full Automation Patterns

### Maximum Automation

```bash
# Complete bypass (zero friction)
codex exec --dangerously-bypass-approvals-and-sandbox "Organize project files"

# Safe automation (sandboxed)
codex exec --full-auto "Refactor module with tests"

# Custom automation
codex exec -a never -s workspace-write "Controlled automation"
```

### Automated Workflows

```bash
#!/bin/bash
# Complete project setup automation

setup_project() {
  local name="$1"
  local type="$2"  # react, node, python, etc.

  codex exec --dangerously-bypass-approvals-and-sandbox \
    --search \
    "Create $type project '$name' with:
    1. Industry-standard directory structure
    2. Configuration files (ESLint, Prettier, etc.)
    3. Git initialization with proper .gitignore
    4. README with setup instructions
    5. CI/CD workflow (GitHub Actions)
    6. Docker setup with multi-stage build
    7. Environment variables template
    8. Comprehensive tests
    9. Documentation"
}

# Usage
setup_project "my-app" "react"
```

### Batch Processing

```bash
#!/bin/bash
# Process multiple files with full automation

batch_process() {
  local pattern="$1"
  local operation="$2"

  codex exec --dangerously-bypass-approvals-and-sandbox \
    --json \
    "For each file matching $pattern:
    1. $operation
    2. Preserve formatting
    3. Run tests
    4. Fix any issues
    Return JSON with changes summary"
}

# Examples
batch_process "*.js" "add JSDoc comments and type hints"
batch_process "*.test.ts" "improve test coverage to 100%"
```

## Tool Categories

### File Operations

```bash
# Read and analyze
codex exec --json "List all functions in ./src with their complexity" > analysis.json

# Modify files
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Add error handling to all async functions in ./src"

# Generate files
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Generate API documentation from code"

# Organize files
codex exec --full-auto "Organize imports and exports across project"
```

### Shell Commands

```bash
# Run tests
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Run all tests and fix failures automatically"

# Install dependencies
codex exec --full-auto "Analyze dependencies and update to latest stable"

# Build and deploy
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Build optimized production bundle and run checks"
```

### Web Search

```bash
# Research-driven development
codex exec --search --dangerously-bypass-approvals-and-sandbox \
  "Research best practices for GraphQL and implement schema"

# Technology comparison
codex exec --search --full-auto \
  "Compare REST vs GraphQL vs gRPC and recommend for our use case"
```

## Safety Patterns

### Backup Before Execution

```bash
#!/bin/bash
backup_and_execute() {
  local task="$1"

  # Git backup
  git stash push -m "pre-codex-$(date +%s)"

  if codex exec --dangerously-bypass-approvals-and-sandbox "$task"; then
    echo "Success! Backup: git stash list"
  else
    echo "Failed! Restoring..."
    git stash pop
    return 1
  fi
}
```

### Scoped Automation

```bash
# Limit to specific directory
codex exec --dangerously-bypass-approvals-and-sandbox \
  -C ./src/auth \
  "Only modify files in this directory"

# Add writable directories
codex exec --dangerously-bypass-approvals-and-sandbox \
  --add-dir ./docs \
  --add-dir ./tests \
  "Can write to workspace, docs, and tests"
```

## Complete Automation Examples

### Automated Testing Workflow

```bash
#!/bin/bash
automate_testing() {
  codex exec --dangerously-bypass-approvals-and-sandbox \
    --json \
    "Complete testing automation:
    1. Analyze code coverage
    2. Generate missing unit tests
    3. Generate integration tests
    4. Generate e2e tests
    5. Run all tests
    6. Fix all failing tests
    7. Achieve 100% coverage
    8. Generate coverage report"
}
```

### Automated Refactoring

```bash
#!/bin/bash
automate_refactoring() {
  local module="$1"

  codex exec --dangerously-bypass-approvals-and-sandbox \
    "Comprehensive refactoring of $module:
    1. Analyze code quality
    2. Apply modern patterns
    3. Improve performance
    4. Add error handling
    5. Update tests
    6. Run all tests
    7. Fix any issues
    8. Generate documentation"
}
```

## Related Skills

- `codex-cli`: Main integration
- `codex-auth`: Authentication
- `codex-chat`: Interactive sessions
- `codex-review`: Code review
- `codex-git`: Git workflows
