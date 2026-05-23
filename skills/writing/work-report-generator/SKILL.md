---
name: work-report-generator
description: 从 git commits 生成日报/周报。触发词：生成报告、工作周报。
---

# Work Report Generator

Generate reports from git history.

## Daily Report

```bash
# Get today's commits
git log --since="midnight" --oneline --no-decorate

# Get changed files
git diff --name-only HEAD@{1.day.ago}..HEAD
```

## Weekly Report

```bash
# Weekly commits
git log --since="1 week ago" --oneline --no-decorate

# Summary
git shortlog -sn --since="1 week ago"
```

## Report Template

```markdown
## $(date +%Y-%m-%d) Report

### Completed
- [item]

### In Progress
- [item]

### Blockers
- None
```
