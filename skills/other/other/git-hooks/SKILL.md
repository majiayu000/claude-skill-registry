---
name: git-hooks
description: Set up and configure Git pre-commit hooks for code quality, secrets scanning, and commit message validation. Use when installing git hooks, configuring pre-commit checks, or enforcing code standards.
---

# Git Hooks Skill

## When to Activate

Activate this skill when:
- Setting up pre-commit hooks
- Configuring commit message validation
- Installing secrets scanners
- Enforcing code quality standards
- Automating pre-push tests

## Quick Installation

```bash
# Use interactive installer (recommended)
./AgentUsage/pre_commit_hooks/install_hooks.sh

# Or manual installation for Python project
cp AgentUsage/pre_commit_hooks/commit-msg .git/hooks/
cp AgentUsage/pre_commit_hooks/pre-commit-python .git/hooks/pre-commit
cp AgentUsage/pre_commit_hooks/pre-commit-secrets-scanner .git/hooks/pre-commit-secrets
cp AgentUsage/pre_commit_hooks/pre-push .git/hooks/
chmod +x .git/hooks/*
```

## Available Hooks

### Core Hooks (All Projects)

| Hook | Purpose |
|------|---------|
| `commit-msg` | Validates conventional commit format |
| `pre-commit-secrets-scanner` | Prevents leaked API keys/secrets |

### Language-Specific

| Hook | Language | Checks |
|------|----------|--------|
| `pre-commit-python` | Python | Black, Ruff |
| `pre-commit-javascript` | JS/TS | Prettier, ESLint, TypeScript |
| `pre-commit-go` | Go | gofmt, go vet |
| `pre-commit-multi-language` | Mixed | Auto-detects and runs appropriate tools |

### Automation Hooks

| Hook | Purpose |
|------|---------|
| `pre-push` | Runs tests before push |
| `post-checkout` | Auto-updates dependencies on branch switch |
| `post-commit` | Shows commit summary and TODOs |

## Hook Selection by Project

```bash
# Python Project
commit-msg + pre-commit-python + pre-commit-secrets-scanner + pre-push

# JavaScript Project
commit-msg + pre-commit-javascript + pre-commit-secrets-scanner + pre-push

# Go Project
commit-msg + pre-commit-go + pre-commit-secrets-scanner + pre-push

# Multi-language
commit-msg + pre-commit-multi-language + pre-commit-secrets-scanner + pre-push
```

## What Each Hook Does

### commit-msg
Validates commit message format:
```bash
# Accepted formats
feat: Add user authentication
fix: Correct validation error
docs(readme): Update installation

# Rejected
Update files  # No type
feat add feature  # Missing colon
```

### pre-commit-secrets-scanner
Scans for exposed secrets:
- Anthropic API keys (`sk-ant-...`)
- OpenAI API keys (`sk-...`)
- AWS credentials (`AKIA...`)
- GitHub tokens (`ghp_...`)
- Hardcoded passwords

### pre-commit-python
```bash
# Runs automatically on staged .py files
uv run black --check $file
uv run ruff check $file
```

### pre-push
```bash
# Runs before push
uv run pytest tests/  # or pnpm test, go test, cargo test
```

## Testing Hooks

```bash
# Test pre-commit directly
.git/hooks/pre-commit

# Test with sample commit
git add .
git commit -m "test: verify hooks"

# Run with debug output
bash -x .git/hooks/pre-commit
```

## Bypassing Hooks (Emergency Only)

```bash
# Skip all hooks
git commit --no-verify -m "Emergency fix"

# Only use when:
# - Emergency production fixes
# - Hook malfunction
# - Intentional override
```

## Troubleshooting

### Hook Not Running

```bash
# Check existence
ls -l .git/hooks/

# Fix permissions
chmod +x .git/hooks/*

# Check syntax
bash -n .git/hooks/pre-commit
```

### Permission Denied

```bash
chmod +x .git/hooks/*
```

### Failed Quality Checks

```bash
# Run tools manually
uv run black --check .
uv run ruff check .

# Fix issues
uv run black .
uv run ruff check --fix .

# Retry commit
git commit -m "Your message"
```

### Missing Tools

```bash
# Install code quality tools
uv add --dev black ruff

# Verify installation
which black
uv run black --version
```

## Custom Hook Configuration

### Modify pre-commit for Your Project

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Get staged Python files
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

if [ -n "$FILES" ]; then
    # Run your tools
    uv run black --check $FILES || exit 1
    uv run ruff check $FILES || exit 1
fi

exit 0
```

## Hook Execution Order

1. **pre-commit** - Before commit (code quality)
2. **commit-msg** - Validates message format
3. **post-commit** - After commit (notifications)
4. **pre-push** - Before push (tests)

## Best Practices

### DO ✅
- Install secrets scanner on ALL projects
- Use commit-msg for consistent history
- Run tests in pre-push
- Test hooks after installation

### DON'T ❌
- Skip hooks regularly
- Disable secrets scanning
- Ignore hook failures
- Commit without testing hooks first

## Related Resources

See `AgentUsage/pre_commit_hooks/` for:
- `setup_guide.md` - Complete installation guide
- `examples.md` - Custom hook examples
- `TROUBLESHOOTING.md` - Common issues
- Individual hook scripts for reference
