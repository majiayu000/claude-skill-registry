---
name: sc-git
description: Git operations with intelligent commit messages and workflow optimization. Use when committing changes, managing branches, or optimizing git workflows.
---

# Git Operations Skill

Intelligent git operations with smart commit generation.

## Quick Start

```bash
# Status analysis
/sc:git status

# Smart commit
/sc:git commit --smart-commit

# Interactive merge
/sc:git merge feature-branch --interactive
```

## Behavioral Flow

1. **Analyze** - Check repository state and changes
2. **Validate** - Ensure operation is appropriate
3. **Execute** - Run git command with automation
4. **Optimize** - Apply smart messages and patterns
5. **Report** - Provide status and next steps

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--smart-commit` | bool | false | Generate conventional commit message |
| `--interactive` | bool | false | Guided operation mode |

## Evidence Requirements

This skill does NOT require hard evidence. Git operations are self-documenting through:
- Commit history
- Branch state
- Repository logs

## Operations

### Status Analysis
```
/sc:git status
# Repository state with change summary
# Actionable recommendations
```

### Smart Commit
```
/sc:git commit --smart-commit
# Analyzes changes
# Generates conventional commit message
# Format: type(scope): description
```

### Branch Operations
```
/sc:git branch feature/new-feature
/sc:git checkout main
/sc:git merge feature-branch
```

### Interactive Operations
```
/sc:git merge feature --interactive
# Guided merge with conflict resolution
# Step-by-step assistance
```

## Commit Message Format

Smart commits follow Conventional Commits:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `refactor` - Code restructuring
- `test` - Test additions
- `chore` - Maintenance

## Examples

### Analyze Changes
```
/sc:git status
# Summary of staged/unstaged changes
# Recommended next actions
```

### Commit with Analysis
```
/sc:git commit --smart-commit
# Scans diff, generates message:
# feat(auth): add JWT token refresh mechanism
```

### Guided Merge
```
/sc:git merge feature/auth --interactive
# Conflict detection and resolution guidance
# Step-by-step assistance
```

## MCP Integration

### PAL MCP (Validation & Review)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__pal__precommit` | Before commit | Comprehensive change validation |
| `mcp__pal__codereview` | Before merge | Code quality review of changes |
| `mcp__pal__consensus` | Merge conflicts | Multi-model resolution strategy |
| `mcp__pal__debug` | Git issues | Investigate repository problems |

### PAL Usage Patterns

```bash
# Pre-commit validation (--smart-commit)
mcp__pal__precommit(
    path="/path/to/repo",
    step="Validating changes before commit",
    findings="Security, completeness, test coverage",
    include_staged=True,
    include_unstaged=False
)

# Review before merge
mcp__pal__codereview(
    review_type="full",
    step="Reviewing feature branch before merge",
    findings="Quality, security, breaking changes",
    compare_to="main"
)

# Consensus on merge conflict resolution
mcp__pal__consensus(
    models=[{"model": "gpt-5.2", "stance": "neutral"}, {"model": "gemini-3-pro", "stance": "neutral"}],
    step="Evaluate: Which conflict resolution preserves intended behavior?"
)
```

### Rube MCP (Automation & Notifications)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__rube__RUBE_SEARCH_TOOLS` | GitHub/GitLab | Find repository management tools |
| `mcp__rube__RUBE_MULTI_EXECUTE_TOOL` | PR/notifications | Create PRs, notify team, update issues |
| `mcp__rube__RUBE_CREATE_UPDATE_RECIPE` | Git workflows | Save reusable git automation |

### Rube Usage Patterns

```bash
# Create PR and notify team after commit
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "GITHUB_CREATE_PULL_REQUEST", "arguments": {
        "repo": "myapp",
        "title": "feat: Add user authentication",
        "body": "## Summary\n- Added JWT auth\n- Added refresh tokens",
        "base": "main",
        "head": "feature/auth"
    }},
    {"tool_slug": "SLACK_SEND_MESSAGE", "arguments": {
        "channel": "#pull-requests",
        "text": "New PR ready for review: feat: Add user authentication"
    }}
])

# Update issue status on merge
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "JIRA_UPDATE_ISSUE", "arguments": {
        "issue_key": "PROJ-123",
        "status": "Done"
    }},
    {"tool_slug": "GITHUB_CREATE_ISSUE_COMMENT", "arguments": {
        "repo": "myapp",
        "issue_number": 456,
        "body": "Merged in PR #789"
    }}
])
```

## Flags (Extended)

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--pal-precommit` | bool | false | Use PAL precommit validation |
| `--pal-review` | bool | false | Use PAL codereview before merge |
| `--create-pr` | bool | false | Create PR via Rube after commit |
| `--notify` | string | - | Notify via Rube (slack, teams, email) |

## Tool Coordination

- **Bash** - Git command execution
- **Read** - Repository state analysis
- **Grep** - Log parsing
- **Write** - Commit message generation
- **PAL MCP** - Pre-commit validation, code review, conflict resolution
- **Rube MCP** - PR creation, team notifications, issue updates
