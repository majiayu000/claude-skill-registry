---
name: git-stats
description: 分析Git仓库统计信息，包括提交、贡献者和代码变更。
metadata:
  short-description: Git仓库统计
source:
  repository: https://github.com/gitpython-developers/GitPython
  license: BSD-3-Clause
---

# Git Stats Tool

## Description
Analyze Git repository statistics including commit history, contributor activity, and code changes.

## Trigger
- `/git-stats` command
- User needs repository analysis
- User wants commit statistics

## Usage

```bash
# Repository overview
python scripts/git_stats.py

# Contributor stats
python scripts/git_stats.py --contributors

# Commit history
python scripts/git_stats.py --commits --since "2024-01-01"

# File changes
python scripts/git_stats.py --files --top 10
```

## Tags
`git`, `stats`, `repository`, `commits`, `analysis`

## Compatibility
- Codex: ✅
- Claude Code: ✅
