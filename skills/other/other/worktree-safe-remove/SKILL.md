---
name: worktree-safe-remove
description: Safely remove a worktree by checking for important data in data/local before deletion. Preserves data/shared (symlink to main repository).
---

# Worktree Safe Remove

Worktree を安全に削除する（重要データのチェック付き）。

## Goal

重要なデータを失わずに worktree を削除する。

## Instructions

1. Worktree 削除前に `data/local/` 内の重要ファイルをチェック
2. 重要ファイルが見つかった場合はユーザーに警告
3. `data/shared/` は保持される（メインリポジトリへの symlink のため）

## Usage

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
"$REPO_ROOT/.agent/skills/worktree-safe-remove/safe-remove.sh" "$WORKTREE_PATH"
```

## Constraints

- 削除前に `data/local/` の重要データを必ずバックアップ
- `data/shared/` は削除されない（全 worktree で共有）
