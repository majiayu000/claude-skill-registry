---
name: headless-cli-agents
description: This skill provides comprehensive guidance for running AI coding agents in non-interactive (headless) mode for automation, CI/CD pipelines, and scripting. Use when integrating Claude Code, Codex, Gemini, OpenCode, Qwen, or Droid CLI into automated workflows where human interaction is not desired.
---

# Headless CLI Agents

## Overview

This skill enables the use of AI coding agents in non-interactive mode for automation scenarios. It provides command references, safety considerations, and practical examples for integrating AI agents into automated workflows.

## Quick Reference

| Agent | Basic Command | Automation Flag | Best For |
|-------|--------------|----------------|----------|
| Claude Code | `claude -p "prompt"` | Auto-approved by default | General coding tasks |
| OpenAI Codex | `codex exec "prompt"` | `--full-auto` | Complex refactoring |
| Google Gemini | `gemini -p "prompt"` | `--yolo` (if available) | Analysis tasks |
| OpenCode | `opencode -p "prompt"` | Auto-approved by default | Multi-provider support |
| Qwen Code | `qwen -p "prompt"` | `--yolo` | Local model support |
| Factory Droid | `droid exec "prompt"` | `--auto <level>` | Controlled automation |

## When to Use Headless Mode

## Core Concepts

### 1. Agent Selection

Choose the appropriate agent based on your requirements:

**Claude Code CLI** - Best for general-purpose coding with excellent code understanding
```bash
# Basic usage
claude -p "Review this code for security issues"

# With additional context
claude -p "Generate tests for authentication module" --add-dir ./tests
```

**OpenAI Codex CLI** - Best for complex refactoring and code transformation or a comprehensive research
```bash
# Automated refactoring
codex exec --full-auto "Refactor this module to use async/await"

# Outside git repos
codex exec --skip-git-repo-check --full-auto "Create API documentation"
```

**Google Gemini CLI** - Best for analysis and documentation tasks
```bash
# Analysis with structured output
gemini -p "Analyze codebase architecture" --output-format json

# Documentation generation
cat src/ | gemini -p "Generate comprehensive API documentation"
```

### 2. Safety and Autonomy Levels

Different agents provide varying levels of automation control:

**Important**: Always specify a timeout of at least 15 minutes for headless commands to prevent hanging

**Read-Only Mode (Safest)**
```bash
# Analysis without changes
droid exec "Analyze security vulnerabilities"
gemini -p "Review code quality metrics"
```

**Low-Risk Changes**
```bash
# Documentation and comments
droid exec "Add docstrings to all functions" --auto low
codex exec --full-auto "Update README with installation instructions"
```

**Development Operations**
```bash
# Package installation, test running
droid exec "Install dependencies and run tests" --auto medium
codex exec --full-auto "Fix failing unit tests"
```

**High-Risk Changes (Use Carefully)**
```bash
# Production deployments, major refactoring
droid exec "Implement OAuth2 migration" --auto high
# Only in isolated environments
codex exec --yolo "Complete system refactoring"
```

### 3. Input/Output Patterns

**Piping Content**
```bash
# Analyze git diff
git diff | claude -p "Review these changes for bugs"

# Process error logs
cat error.log | qwen -p "Categorize and summarize these errors"

# Multiple files
find . -name "*.py" | xargs claude -p "Check for anti-patterns"
```

**File-based Prompts**
```bash
# Read from prompt file
droid exec -f migration_prompt.md

# JSON output for parsing
gemini -p "List all API endpoints" --output-format json
```

**Structured Output**
```bash
# Machine-readable output
opencode -p "Count lines of code" -f json
claude -p "Generate test coverage report" > coverage_report.md
```

Important to know for Claude Code!
When you use `Bash` tool, you have to specify the timeout at least 15 min when you attempt to run any of these headless cli agents

## Common Workflows

### Code Review Automation
```bash
# Quick security scan
find . -name "*.py" | xargs claude -p "Check for security vulnerabilities"

# Performance analysis
git diff | codex exec --full-auto "Analyze performance impact of changes"

# Documentation consistency
droid exec "Verify all functions have docstrings" --auto low
```

### Test Generation
```bash
# Unit tests for specific module
claude -p "Generate comprehensive unit tests for auth.py using pytest"

# Integration tests
codex exec --full-auto "Create API integration tests with realistic data"

# Test coverage analysis
qwen -p "Analyze test coverage and suggest missing test cases"
```

### Documentation Automation
```bash
# API documentation
find src/ -name "*.py" | gemini -p "Generate OpenAPI specification"

# README generation
claude -p "Create comprehensive README with setup, usage, and examples"

# Changelog from commits
git log --oneline | qwen -p "Generate changelog from commit history"
```

## Integration Patterns

### CI/CD Integration

**GitHub Actions**
```yaml
- name: AI Code Review
  run: |
    git diff origin/main...HEAD | claude -p "Review for security and performance issues"
```

**GitLab CI**
```yaml
script:
  - gemini -p "Generate test suite for new features" --output-format json > test_plan.json
```

### Pre-commit Hooks
```bash
#!/bin/sh
# .git/hooks/pre-commit
git diff --cached | claude -p "Check staged changes for obvious bugs"
if [ $? -ne 0 ]; then exit 1; fi
```

### Monitoring and Alerts
```bash
# Daily code quality report
claude -p "Generate daily code quality report" | mail -s "Code Quality" team@example.com
```

## Troubleshooting

### Common Issues

**Agent not found**: Ensure CLI tools are installed and in PATH
```bash
which claude codex gemini opencode qwen droid
```

**Authentication errors**: Verify API keys and tokens
```bash
claude auth status
codex auth verify
```

**Permission denied**: Check file permissions and working directory
```bash
ls -la
pwd
```

**Context limit exceeded**: Reduce analysis scope or use specific files
```bash
# Instead of entire codebase
claude -p "Analyze main.py only"

# Or use specific patterns
find src/ -name "*.py" -maxdepth 2 | claude -p "Review these files"
```

### Debug Mode
Most agents support verbose output:
```bash
claude --verbose -p "Debug prompt"
codex exec --debug "Debug task"
```

## Resources

### references/

**agent-specific-commands.md** - Detailed command documentation for all six CLI agents including flags, options, and specific usage patterns. Load this when you need comprehensive syntax reference for a particular agent.
