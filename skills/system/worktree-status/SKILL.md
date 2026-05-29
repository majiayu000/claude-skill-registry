---
name: worktree-status
description: worktreeとtmuxセッションの状態確認。「worktreeの状況を見たい」「実行中プロセスを確認」時に使用
---

# Worktree状態確認

gwqを使ってworktreeとプロセスの状態を確認します。

## 手順

1. 現在のリポジトリのworktree一覧:
   ```bash
   gwq list -v
   ```

2. 全リポジトリのworktree一覧:
   ```bash
   gwq list -g
   ```

3. 全worktreeの状態（変更ファイルなど）:
   ```bash
   gwq status
   ```

4. 実行中プロセス情報付き:
   ```bash
   gwq status -g --show-processes
   ```

5. tmuxセッション一覧:
   ```bash
   gwq tmux list
   ```

## オプション
- 監視モード（自動更新）: `gwq status -w`
- 特定worktreeの詳細: `gwq get <pattern>`

## 出力例
```
gwq status -g --show-processes
────────────────────────────────────
repo: frontend
  feature/ui [modified: 3 files]
    └─ tmux: npm run dev (pid: 12345)

repo: backend
  feature/api [clean]
    └─ tmux: go run main.go (pid: 12346)
```
