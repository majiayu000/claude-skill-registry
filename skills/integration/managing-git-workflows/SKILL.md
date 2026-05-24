---
name: managing-git-workflows
description: >
  Gitワークフロー自動化パターン：ブランチ命名、コミットメッセージ、PR説明、Issue作成。
  一貫したGit操作のためのテンプレートと規約を提供。
  トリガー: git, branch, commit, pull request, PR, issue, conventional commits, ブランチ命名。
allowed-tools: Bash, Read, Grep, Glob
user-invocable: false
---

# Git ワークフロー管理

Conventional Commitsと一貫した命名規則を使用したGitワークフロー自動化パターン。

## 目的

個々のコマンドに埋め込まれていたGitワークフローパターンを集約。
コマンドはGit操作のためにこのスキルを参照する薄いオーケストレーターとなる。

## ワークフローリファレンス

| ワークフロー       | リファレンス                                                                                                                            | コマンド |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| ブランチ命名       | [@../../skills/managing-git-workflows/references/branch-naming.md](../../skills/managing-git-workflows/references/branch-naming.md)     | /branch  |
| コミットメッセージ | [@../../skills/managing-git-workflows/references/commit-messages.md](../../skills/managing-git-workflows/references/commit-messages.md) | /commit  |
| PR説明             | [@../../skills/managing-git-workflows/references/pr-descriptions.md](../../skills/managing-git-workflows/references/pr-descriptions.md) | /pr      |
| Issue作成          | [@../../skills/managing-git-workflows/references/issue-templates.md](../../skills/managing-git-workflows/references/issue-templates.md) | /issue   |

## クイックリファレンス

### ブランチ命名規約

```text
<type>/<ticket>-<description>

例:
  feat/AUTH-123-oauth-login
  fix/BUG-456-null-pointer
  refactor/TECH-789-cleanup-utils
```

### Conventional Commits

```text
<type>(<scope>): <description>

[オプションの本文]

[オプションのフッター]
```

| タイプ     | 目的                   |
| ---------- | ---------------------- |
| `feat`     | 新機能                 |
| `fix`      | バグ修正               |
| `docs`     | ドキュメント           |
| `refactor` | コードリファクタリング |
| `test`     | テスト変更             |
| `chore`    | ビルド/ツール          |

### PR説明テンプレート

```markdown
## Summary

- [1-3 bullet points]

## Changes

- [Key changes]

## Test Plan

- [ ] Unit tests added
- [ ] Manual testing done
```

### Issueテンプレート

```markdown
## Description

[Clear description]

## Steps to Reproduce (for bugs)

1. [Step 1]
2. [Step 2]

## Expected vs Actual

- Expected: [behavior]
- Actual: [behavior]
```

## ベストプラクティス

### 安全第一

- `git push --force` は使用しない（`--force-with-lease` を使用）
- `git reset --hard` は確認なしに使用しない
- コミット前に必ず `git status` を確認

### アトミックコミット

1コミット1論理変更:

```bash
# 悪い例
git commit -m "fix bug and add feature"

# 良い例
git commit -m "fix(auth): resolve token refresh"
git commit -m "feat(user): add profile page"
```

## 参照

### 原則 (rules/)

- [@../../rules/core/AI_OPERATION_PRINCIPLES.md](../../rules/core/AI_OPERATION_PRINCIPLES.md) - 安全第一

### 関連スキル

- `utilizing-cli-tools` - CLIツール使用パターン

### 使用元コマンド

- `/branch` - ブランチ名提案
- `/commit` - コミットメッセージ生成
- `/pr` - PR説明生成
- `/issue` - Issue作成
