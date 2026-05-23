---
name: utilizing-cli-tools
description: >
  CLI tools guide for git, gh, npm, and other development tools.
  Triggers: git, gh, npm, CLI, コマンドライン, バージョン管理, ブランチ, コミット.
allowed-tools: [Bash, Read, Glob]
user-invocable: false
---

# CLIツールガイド

## 参照

| カテゴリ       | リファレンス                                                      |
| -------------- | ----------------------------------------------------------------- |
| バージョン管理 | [@./references/git-essentials.md](./references/git-essentials.md) |
| GitHub         | [@./references/gh-github-cli.md](./references/gh-github-cli.md)   |
| パッケージ管理 | [@./references/npm-scripts.md](./references/npm-scripts.md)       |

## クイックリファレンス

### Git

| アクション | コマンド                    |
| ---------- | --------------------------- |
| ステータス | `git status --short`        |
| Diff       | `git diff --staged`         |
| ブランチ   | `git branch --show-current` |
| ログ       | `git log --oneline -10`     |

### HEREDOCコミット

```bash
git commit -m "$(cat <<'EOF'
feat(auth): OAuth認証を追加
EOF
)"
```
