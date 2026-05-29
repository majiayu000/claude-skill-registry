---
name: worktree-dev
description: worktreeでtmuxセッションを使って開発サーバーを起動。「開発サーバーを立ち上げたい」「バックグラウンドでプロセス実行」時に使用
argument-hint: <worktree-pattern> <command>
---

# Worktree開発サーバー起動

gwq tmuxを使ってworktreeで長時間実行プロセスをバックグラウンド起動します。

## 引数
- `$ARGUMENTS`: `<worktree-pattern> <command>` 形式
  - 例: `feature/new-feature "npm run dev"`

## 手順

1. worktreeでコマンドをtmuxセッションで起動:
   ```bash
   gwq tmux run -w <worktree-pattern> "<command>"
   ```

2. セッション一覧確認:
   ```bash
   gwq tmux list
   ```

3. セッションにアタッチ（ログ確認など）:
   ```bash
   gwq tmux attach <pattern>
   ```

## オプション
- カスタムセッションID: `gwq tmux run --id <name> "<command>"`
- アタッチしたまま実行: `gwq tmux run --no-detach "<command>"`
- 完了時自動削除: `gwq tmux run --auto-cleanup "<command>"`

## 例
```bash
# フロントエンド開発サーバー
gwq tmux run -w feature/ui "npm run dev"

# バックエンドサーバー
gwq tmux run -w feature/api "go run main.go"

# テスト監視
gwq tmux run -w feature/test "npm run test:watch"
```
