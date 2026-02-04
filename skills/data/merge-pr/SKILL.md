---
name: merge-pr
description: "PR をマージし、worktree とローカルブランチをクリーンアップする。トリガー: /merge-pr, PRマージ, worktreeクリーンアップ"
user-invocable: true
allowed-tools: Bash
---

# /merge-pr

PRマージとworktreeクリーンアップを一括実行。

## 使い方

```
/merge-pr 42
```

## 実行フロー

1. 現在のworktreeパスとブランチ名を取得
2. メインリポジトリに移動
3. worktree削除: `git worktree remove <path>`
4. ローカルブランチ削除: `git branch -D <branch>`
5. PRマージ: `gh pr merge <num> --merge --delete-branch`
6. main更新: `git pull origin main`

## 注意

- worktree内から実行した場合、自動でメインリポに移動する
- マージ前に未コミットの変更がないことを確認する
