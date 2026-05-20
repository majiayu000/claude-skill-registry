---
name: worktree
description: Planが複雑/完了した直後に自動的に呼び出す必要があるスキルです
model: haiku
---

git worktree を作成して並列作業を可能にします。

## 作成手順
1. **現在位置を記録**: `PROJECT_ROOT=$(pwd)` として保存
2. `git worktree add ../<branch-name> -b <branch-name>`
3. branch名にslashは使わないこと（例: feature-auth ✓, feature/auth ✗）
4. 必要なら `pnpm install` を実行（判断基準: package.jsonに変更がある場合）

## 作業中の迷子防止（重要）
各コマンド実行前に `pwd` で現在位置を確認し、意図したディレクトリにいることを確認する。

## 完了時の手順（必須）
作業完了後は必ず以下を実行：

1. **ルートに戻る**: `cd $PROJECT_ROOT` （絶対パスで戻る）
2. **現在位置確認**: `pwd` で正しいディレクトリにいることを確認
3. **クリーンアップ**: `git worktree remove ../<branch-name>`
4. **残存確認**: `git worktree list` でworktreeが残っていないことを確認

## 注意
- worktree ごとに node_modules が必要になる場合がある
- 長期間放置するとディスクを圧迫する
- 作業完了時のクリーンアップを忘れないこと
- **迷子になったら**: `git worktree list` で全worktreeの場所を確認
