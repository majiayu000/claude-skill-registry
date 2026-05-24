---
name: pr-and-cleanup
description: worktree での開発完了後に PR を作成し、worktree を自動削除する。ローカル/リモートブランチは保持。
---

# PR And Cleanup

worktreeでの開発完了後、PR作成と同時にworktreeを自動的にクリーンアップします。

## 概要

このスキルは以下を自動で実行します:

1. 現在のworktreeディレクトリとブランチを検出
2. 未コミットの変更がないか確認
3. PRを作成（タイトル・本文はインタラクティブ入力可能）
4. PR作成成功後、worktreeを削除
5. mainブランチ（リポジトリルート）にチェックアウト

**重要**: ローカルブランチとリモートブランチは残ります（削除されません）

## 使用方法

### 基本的な使い方

```bash
cd .worktrees/<feature-name>
bash ../../.claude/skills/pr-and-cleanup/scripts/pr_and_cleanup.sh
```

### オプション

```bash
# PR作成のみ（worktreeを削除しない）
bash pr_and_cleanup.sh --pr-only

# worktreeクリーンアップのみ（PR作成済みの場合）
bash pr_and_cleanup.sh --cleanup-only

# タイトルと本文を事前指定
bash pr_and_cleanup.sh --title "feat: Add new feature" --body "詳細な説明..."

# ドラフトPRとして作成
bash pr_and_cleanup.sh --draft

# 未コミット変更を無視（非推奨）
bash pr_and_cleanup.sh --force
```

## 前提条件

- worktreeディレクトリ内で実行すること
- すべての変更がコミット済みであること
- `gh` CLI がインストール・認証済みであること
- リモートブランチにpush済みであること（またはgh pr createが自動push）

## 実行例

```bash
$ cd .worktrees/issue-42-auth
$ bash ../../.claude/skills/pr-and-cleanup/scripts/pr_and_cleanup.sh

[INFO] Current branch: feature/issue-42-auth
[INFO] Worktree path: /path/to/.worktrees/issue-42-auth
[STEP] Checking for uncommitted changes...
[INFO] No uncommitted changes detected
[STEP] Creating pull request...
[INFO] PR created: https://github.com/user/repo/pull/123
[STEP] Removing worktree...
[INFO] Worktree removed successfully
[STEP] Returning to main branch...
[INFO] Now on branch: main
```

## エラーハンドリング

### 未コミットの変更がある場合
スクリプトは停止し、コミットを促します。

### PR作成失敗時
worktreeは削除されず、現在のディレクトリに留まります。

### worktree外で実行した場合
警告を表示し、処理を中止します。

## 関連スキル

- `create-worktree`: worktree作成
- `worktree-workflow`: ワークフロー全体の概要

## 詳細

詳細については [REFERENCE.md](REFERENCE.md) を参照してください。
