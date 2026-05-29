---
name: multi-repo-dev
description: ghq・gwq・tmuxを使った複数リポジトリでの並行開発セットアップ。「複数リポジトリで同時に開発」「マイクロサービス開発」時に使用
---

# 複数リポジトリ並行開発

ghq・gwq・tmuxを組み合わせて複数リポジトリで並行開発を行います。

## ワークフロー

### 1. リポジトリの取得
```bash
# リポジトリをclone（既にあればスキップ）
ghq get github.com/user/frontend-repo
ghq get github.com/user/backend-repo
```

### 2. 各リポジトリでworktree作成
```bash
# フロントエンド
cd $(ghq list -p | grep frontend-repo) && gwq add -b feature/api-integration

# バックエンド
cd $(ghq list -p | grep backend-repo) && gwq add -b feature/new-endpoint
```

### 3. 各worktreeで開発サーバー起動
```bash
gwq tmux run -w feature/api-integration "npm run dev"
gwq tmux run -w feature/new-endpoint "go run main.go"
```

### 4. 状態確認
```bash
# 全リポジトリのworktree状態
gwq status -g --show-processes

# tmuxセッション一覧
gwq tmux list
```

### 5. 特定worktreeでコマンド実行
```bash
gwq exec feature/api-integration -- npm test
gwq exec feature/new-endpoint -- go test ./...
```

## ghqコマンド参考
```bash
ghq list              # リポジトリ一覧
ghq list -p           # フルパスで表示
ghq root              # ルートディレクトリ
ghq get <url>         # リポジトリ取得
```

## Tips
- `gwq status -w` で監視モード（変更を自動検知）
- `gwq tmux attach <pattern>` でセッションにアタッチ
- 作業完了後は `gwq tmux kill` → `gwq remove -b` でクリーンアップ
