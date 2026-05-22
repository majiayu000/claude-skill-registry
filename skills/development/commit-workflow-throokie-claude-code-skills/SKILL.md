---
name: commit-workflow
description: 生成规范的 Git commit 消息，处理 Git 工作流。触发词：commit、提交代码、git commit。
disable-model-invocation: true
allowed-tools: Bash, Read
---

# Commit Workflow

Generate conventional commit messages following best practices.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `perf` | Performance improvement |
| `test` | Adding/updating tests |
| `chore` | Build, config, dependencies |
| `ci` | CI/CD changes |
| `revert` | Revert previous commit |

## Workflow

### 1. Analyze Changes

```bash
git status
git diff --cached
git diff
git log --oneline -5
```

### 2. Stage Changes

```bash
# Stage specific files
git add <files>

# Or stage all
git add -A
```

### 3. Generate Commit Message

Based on the changes:
1. Identify the type of change
2. Determine the scope (optional)
3. Write a concise subject (50 chars max)
4. Add body if needed (explain why, not what)
5. Reference issues in footer

### 4. Execute Commit

```bash
git commit -m "type(scope): subject"

# Or with body
git commit -m "type(scope): subject" -m "Body paragraph 1" -m "Body paragraph 2"
```

## Examples

```bash
# Feature
git commit -m "feat(auth): add OAuth2 login support"

# Bug fix
git commit -m "fix(api): handle null response in user endpoint"

# With body and footer
git commit -m "feat(dashboard): add real-time metrics" -m "Implements WebSocket connection for live data updates. Includes reconnection logic and error handling." -m "Closes #123"

# Breaking change
git commit -m "feat(api)!: change user endpoint response format" -m "BREAKING CHANGE: User endpoint now returns nested object instead of flat structure"
```

## Commit Best Practices

1. **One logical change per commit** - Don't mix unrelated changes
2. **Write imperative mood** - "add feature" not "added feature"
3. **No period at end** of subject line
4. **Capitalize first letter** of subject
5. **Separate subject from body** with blank line
6. **Wrap body at 72 characters**
7. **Use body to explain why**, not what
8. **Reference issues** in footer

## Pre-commit Checklist

- [ ] All tests pass
- [ ] No debug code left
- [ ] No sensitive data in changes
- [ ] Commit message follows format
- [ ] Changes are logically grouped