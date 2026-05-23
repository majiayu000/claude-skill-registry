---
name: create-pr
description: Create and push PR with auto-generated title and description
model: haiku
allowed-tools: Bash(git :*), Bash(gh :*)
---

# Create PR

Create pull request with concise, meaningful description.

## Context

- Current branch: !`git branch --show-current`
- Working tree status: !`git status --short`
- Recent commits: !`git log --oneline -5`
- Remote tracking: !`git rev-parse --abbrev-ref @{upstream} 2>/dev/null || echo "none"`

## Workflow

1. **Verify**: Check `git status` and current branch
2. **Branch Safety**: **CRITICAL** - If on main/master, create descriptive branch from changes
3. **Push**: `git push -u origin HEAD`
4. **Analyze**: `git diff origin/main...HEAD --stat`
5. **Generate PR**:
   - Title: One-line summary (max 72 chars)
   - Body: Bullet points of key changes
6. **Submit**: `gh pr create --title "..." --body "..."`
7. **Return**: Display PR URL

## PR Format

```markdown
## Summary

• [Main change or feature]
• [Secondary changes]
• [Any fixes included]

## Type

[feat/fix/refactor/docs/chore]
```

## Rules

- NO verbose descriptions
- NO "Generated with" signatures
- Auto-detect base branch (main/master/develop)
- Use HEREDOC for multi-line body
- If PR exists, return existing URL

User: $ARGUMENTS
