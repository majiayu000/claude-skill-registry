---
name: worktree-init
description: Initialize worktree data protection configuration. Run this once in the main repository before creating any worktrees to set up shared data storage.
---

# Worktree Init

Worktree データ保護設定を初期化する。

## Goal

全 worktree で共有されるデータストレージの場所を設定する。

## Instructions

1. **メインリポジトリで一度だけ**実行する（worktree 作成前に）
2. 全 worktree で共有される `data/shared/` ディレクトリ構造を初期化する

## Usage

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
"$REPO_ROOT/.agent/skills/worktree-init/init.sh"
```

## Constraints

- メインリポジトリでのみ実行（worktree 内では実行しない）
- リポジトリルートへの書き込み権限が必要
