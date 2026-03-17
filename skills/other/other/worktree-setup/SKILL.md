---
name: worktree-setup
description: Automatically invoked after `git worktree add` to create data/shared symlink and data/local directory. Required before starting work in any new worktree.
---

# Worktree Setup

新しい worktree にデータディレクトリ構造をセットアップする。

## Goal

Worktree 作成後に適切なデータディレクトリ構造を設定し、データ保護を確保する。

## Instructions

1. このスキルは `git worktree add` の**後に**実行する
2. 以下を作成:
   - `data/shared/` - メインリポジトリの共有データへの symlink（永続）
   - `data/local/` - worktree 固有の一時ディレクトリ

## Usage

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
"$REPO_ROOT/.agent/skills/worktree-setup/setup.sh"
```

## Constraints

- 事前にメインリポジトリで `worktree-init` を実行しておくこと
- worktree ディレクトリ内で実行すること
