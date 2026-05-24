---
name: worktree-create
description: 新しいブランチとworktreeを作成し、開発作業を開始するためのスキル。タスク着手時に「worktreeを作成」「ブランチを作成して作業開始」「/worktree-create <branch-name>」などで使用。
---

# Worktree Create

新規タスクの作業を開始する際に、ブランチとworktreeを作成するスキル。

## 使用タイミング

- 新しいタスクに着手する時
- 機能開発やバグ修正を開始する時
- 独立した作業ディレクトリが必要な時

## 引数

```
/worktree-create <branch-name>
```

- `<branch-name>`: 作成するブランチ名（例: `feature/add-user-auth`, `fix/login-bug`）

## ブランチ命名規則

| プレフィックス | 用途 |
|--------------|------|
| `feature/` | 新機能 |
| `fix/` | バグ修正 |
| `refactor/` | リファクタリング |
| `docs/` | ドキュメント |

## 実行手順

### 1. 現在の状態を確認

```bash
# 現在のブランチと未コミットの変更を確認
git status
git worktree list
```

### 2. Worktreeを作成

```bash
# mainブランチから新しいworktreeを作成
git worktree add ../Lorepedia-<branch-name> -b <branch-name> main
```

### 3. 環境変数ファイルのシンボリックリンク作成

worktree間で`.env`を共有するため、メインリポジトリの`.env`へシンボリックリンクを作成:

```bash
cd ../Lorepedia-<branch-name>

# メインリポジトリ（最初のworktree）のパスを動的に取得してリンク
MAIN_REPO=$(git worktree list --porcelain | grep "^worktree " | head -1 | sed 's/worktree //')
ln -s "$MAIN_REPO/.env" .env
```

### 4. 依存関係のインストール

worktreeディレクトリでは`node_modules`が共有されないため、必要に応じてインストール:

```bash
pnpm install
```

### 5. 作業開始の案内

worktree作成後、以下を案内する:
- 作業ディレクトリのパス
- 次のステップ（実装開始）

## 注意事項

- 未コミットの変更がある場合は、先にコミットまたはスタッシュする
- 同名のブランチが既に存在する場合はエラーになる
- worktree作成後は新しいディレクトリで作業を継続する

## 実行例

```
User: /worktree-create feature/add-world-list
```

Assistant:
1. git status で現在の状態を確認
2. git worktree add ../Lorepedia-feature-add-world-list -b feature/add-world-list main を実行
3. ln -s でメインリポジトリの.envへシンボリックリンクを作成
4. pnpm install を実行
5. 作業ディレクトリ: /path/to/Lorepedia-feature-add-world-list
   次のステップ: 実装を開始してください
```
