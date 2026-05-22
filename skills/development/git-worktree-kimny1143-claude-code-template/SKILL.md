# git-worktree - Git Worktree 操作

複数ブランチを同時に作業するための Git worktree 管理。

---

## 概要

Git worktree を使うと、1つのリポジトリから複数の作業ディレクトリを作成できる。

**メリット**:
- ブランチ切り替えなしで複数機能を並行開発
- PRレビュー中に別作業が可能
- 本番ホットフィックスと開発を同時進行

---

## 基本コマンド

### Worktree 作成

```bash
# 新規ブランチで作成
git worktree add ../project-feature-x feature-x

# 既存ブランチで作成
git worktree add ../project-hotfix hotfix/urgent-fix

# リモートブランチをチェックアウト
git worktree add ../project-review origin/feature-y
```

### Worktree 一覧

```bash
git worktree list
```

出力例:
```
/path/to/project          abc1234 [main]
/path/to/project-feature  def5678 [feature-x]
/path/to/project-hotfix   ghi9012 [hotfix/urgent-fix]
```

### Worktree 削除

```bash
# 作業ディレクトリを削除
rm -rf ../project-feature-x

# Git から登録解除
git worktree prune
```

または一括:
```bash
git worktree remove ../project-feature-x
```

---

## ワークフロー例

### 1. 機能開発中にホットフィックス

```bash
# 現在: feature-x ブランチで開発中
# 緊急: 本番バグ発生

# ホットフィックス用 worktree 作成
git worktree add ../project-hotfix -b hotfix/login-fix main

# ホットフィックス作業
cd ../project-hotfix
# ... 修正 ...
git commit -m "fix: resolve login issue"
git push origin hotfix/login-fix

# 元の作業に戻る
cd ../project
# feature-x の作業を継続
```

### 2. PRレビュー

```bash
# レビュー対象のブランチを worktree で開く
git fetch origin
git worktree add ../project-review origin/feature-y

# レビュー
cd ../project-review
npm install
npm run dev

# レビュー完了後
cd ../project
git worktree remove ../project-review
```

---

## ベストプラクティス

### ディレクトリ命名

```
project/              # メイン (main)
project-feature-x/    # 機能開発
project-hotfix/       # ホットフィックス
project-review/       # PRレビュー
```

### 定期クリーンアップ

```bash
# 不要な worktree を確認
git worktree list

# マージ済みブランチの worktree を削除
git worktree remove ../project-merged-feature

# 孤立した worktree を整理
git worktree prune
```

### 注意点

1. **同じブランチを複数 worktree で開けない**
2. **node_modules は各 worktree で別途インストール必要**
3. **.env ファイルもコピーが必要**

---

## トラブルシューティング

### "already checked out" エラー

```bash
# 別の worktree で使用中のブランチ
git worktree list  # どこで使われているか確認
```

### 孤立した worktree

```bash
# ディレクトリを手動削除した場合
git worktree prune
```

### ブランチ削除時

```bash
# worktree で使用中のブランチは削除できない
# 先に worktree を削除する
git worktree remove ../project-feature
git branch -d feature
```
