---
name: commit
scope: universal
description: "[UDS] Generate commit messages following Conventional Commits standard"
allowed-tools: Read, Grep, Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*)
argument-hint: "[description of changes | 變更描述]"
disable-model-invocation: true
---

# Commit Message Assistant | Commit Message 助手

Generate well-formatted commit messages following the Conventional Commits standard.

根據 staged 的變更，產生符合 Conventional Commits 格式的 commit message。

## Workflow | 工作流程

1. **Check status** - Run `git status` and `git diff --staged` to understand changes
2. **Analyze changes** - Determine the type (feat, fix, refactor, etc.) and scope
3. **Generate message** - Create a commit message following the format below
4. **Confirm and commit** - Ask user to confirm before executing `git commit`

### Message Format | 訊息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Commit Types | 提交類型

| Type | When to Use | 使用時機 |
|------|-------------|---------|
| `feat` | New feature | 新功能 |
| `fix` | Bug fix | 修復錯誤 |
| `refactor` | Code refactoring | 重構（無功能變更） |
| `docs` | Documentation | 文件更新 |
| `style` | Formatting | 格式調整（無邏輯變更） |
| `test` | Tests | 測試相關 |
| `perf` | Performance | 效能優化 |
| `chore` | Maintenance | 維護任務 |

## Rules | 規則

- **Subject**: imperative mood, no period, first letter capitalized, ≤ 72 characters
- **Body**: explain **WHY** the change was made, not just what changed
- **Footer**: use `BREAKING CHANGE:` for breaking changes, `Fixes #123` for issue refs

## Usage | 使用方式

- `/commit` - Auto-analyze staged changes and suggest commit message
- `/commit fix login bug` - Generate message based on provided description

## Reference | 參考

- Detailed guide: [guide.md](./guide.md)
- Core standard: [commit-message-guide.md](../../core/commit-message-guide.md)
