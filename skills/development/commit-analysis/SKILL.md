---
name: commit-analysis
description: |
  Automated commit analysis and regression detection for AItrader. 自动化提交分析和回归检测。

  Use this skill when:
  - Running regression checks after code changes (代码修改后运行回归检测)
  - Analyzing git commit history (分析 git 提交历史)
  - Using AI to analyze code changes (使用 AI 分析代码变更)
  - Checking if fix commits are still correctly applied (检查修复是否正确应用)
  - Before merging PRs (合并 PR 前)

  Keywords: commit, regression, analysis, git, fix, validation, AI, 提交, 回归, 分析
---

# Commit Analysis & Regression Detection

## Overview

Automated tools for detecting regressions and analyzing code changes:

| Tool | Purpose | Speed |
|------|---------|-------|
| **scripts/smart_commit_analyzer.py** | Auto-evolving regression detection | Fast |
| **scripts/analyze_commits_ai.py** | AI semantic analysis (DeepSeek) | Slow |
| **scripts/analyze_git_changes.py** | Git history statistics | Fast |
| **scripts/validate_commit_fixes.py** | Legacy manual rules (deprecated) | Fast |

## Recommended Tool: smart_commit_analyzer.py

**This is the primary regression detection tool.** Rules are automatically generated from git history.

### Commands

```bash
# Full analysis (update rules + validate)
python3 scripts/smart_commit_analyzer.py

# Update rules only (scan git for new fixes)
python3 scripts/smart_commit_analyzer.py --update

# Validate only (check existing rules)
python3 scripts/smart_commit_analyzer.py --validate

# Show all rules
python3 scripts/smart_commit_analyzer.py --show-rules

# JSON output (for CI/CD)
python3 scripts/smart_commit_analyzer.py --json
```

### Expected Output

```
🔍 Smart Commit Analyzer
============================================================

Step 1: 从 Git 历史更新规则库...
📊 扫描到 78 个修复提交
✅ 新增 5 条规则

Step 2: 验证所有规则...

============================================================
📋 验证结果
============================================================
✅ 通过: 70
❌ 失败: 2
⚠️  警告: 3
⏭️  跳过: 0
```

### How It Works

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: git log --grep="fix"                           │
│          → Auto-discover all fix commits                │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 2: git show <commit> -- <file>                    │
│          → Extract key code patterns from diffs         │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 3: Save to configs/auto_generated_rules.json      │
│          → Rules auto-grow with new fix commits         │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Step 4: Validate all rules                             │
│          → Detect regressions (missing patterns)        │
└─────────────────────────────────────────────────────────┘
```

## AI Deep Analysis (Optional)

Requires `DEEPSEEK_API_KEY` environment variable.

```bash
# Analyze last 10 commits with AI
python3 scripts/analyze_commits_ai.py --commits 10

# JSON output
python3 scripts/analyze_commits_ai.py --commits 10 --json
```

## Git History Analysis

```bash
# Analyze last 50 commits
python3 scripts/analyze_git_changes.py

# Show only fix commits
python3 scripts/analyze_git_changes.py --fix-only

# Analyze more commits
python3 scripts/analyze_git_changes.py --commits 100
```

## GitHub Actions Integration

These tools run automatically on every push/PR via `.github/workflows/commit-analysis.yml`:

| Job | Tool | Trigger |
|-----|------|---------|
| Smart Regression Detection | scripts/smart_commit_analyzer.py | Always |
| AI Deep Analysis | scripts/analyze_commits_ai.py | If DEEPSEEK_API_KEY set |

## Key Files

| File | Purpose |
|------|---------|
| `scripts/smart_commit_analyzer.py` | Main regression detection tool |
| `configs/auto_generated_rules.json` | Auto-generated validation rules |
| `scripts/analyze_commits_ai.py` | AI-powered analysis |
| `scripts/analyze_git_changes.py` | Git history parser |
| `.github/workflows/commit-analysis.yml` | GitHub Actions workflow |

## When to Run

- **Before committing**: `python3 scripts/smart_commit_analyzer.py`
- **Before merging PR**: Automatic via GitHub Actions
- **After pulling updates**: `python3 scripts/smart_commit_analyzer.py --validate`
- **Investigating regressions**: `python3 scripts/smart_commit_analyzer.py --show-rules`

## Interpreting Results

| Status | Meaning | Action |
|--------|---------|--------|
| ✅ Passed | Pattern found in code | None |
| ❌ Failed | Pattern missing (potential regression) | Investigate |
| ⚠️ Warning | Pattern may have been refactored | Review |
| ⏭️ Skipped | File not found (renamed/deleted) | Update rules |
