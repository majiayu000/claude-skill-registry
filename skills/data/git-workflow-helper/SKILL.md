---
name: git-workflow-helper
description: Guide Git workflows including branching, merging, rebasing, and conflict resolution. Use when managing Git operations or resolving complex Git scenarios.
---

# Git Workflow Helper Skill

Gitワークフローを支援するスキルです。

## 概要

Git操作のベストプラクティス、コマンド生成、トラブルシューティングを提供します。

## 主な機能

- **ワークフロー提案**: GitFlow、GitHub Flow、Trunk-Based
- **コマンド生成**: 複雑な操作の安全なコマンド
- **コンフリクト解決**: マージコンフリクトの解決支援
- **歴史の整理**: rebase、squash、cherry-pick
- **トラブルシューティング**: よくある問題の解決
- **フック生成**: pre-commit、pre-push等

## 使用方法

```
以下の操作のGitコマンドを生成：
- ブランチを作成
- 変更をコミット
- リモートにプッシュ
- プルリクエスト作成の準備
```

## ワークフローパターン

### GitHub Flow

```bash
# 1. 最新のmainブランチを取得
git checkout main
git pull origin main

# 2. 機能ブランチを作成
git checkout -b feature/user-authentication

# 3. 変更を加えてコミット
git add .
git commit -m "Add user authentication"

# 4. リモートにプッシュ
git push -u origin feature/user-authentication

# 5. プルリクエストを作成（GitHubで）

# 6. レビュー後、mainにマージ
# 7. ブランチを削除
git branch -d feature/user-authentication
```

### Git Flow

```bash
# develop ブランチから機能ブランチを作成
git checkout develop
git checkout -b feature/new-feature

# 完了後、developにマージ
git checkout develop
git merge --no-ff feature/new-feature

# リリースブランチ
git checkout -b release/1.2.0 develop

# リリース準備完了
git checkout main
git merge --no-ff release/1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
```

## よく使うコマンド

### 変更の取り消し

```bash
# ステージング取り消し
git reset HEAD <file>

# ローカル変更を破棄
git checkout -- <file>

# 直前のコミットを修正
git commit --amend

# コミットを取り消し（変更は保持）
git reset --soft HEAD~1

# コミットを完全に取り消し
git reset --hard HEAD~1
```

### ブランチ操作

```bash
# ブランチ一覧
git branch -a

# リモートブランチを削除
git push origin --delete <branch-name>

# ローカルブランチを削除
git branch -d <branch-name>

# 強制削除
git branch -D <branch-name>

# ブランチ名変更
git branch -m <old-name> <new-name>
```

### コンフリクト解決

```bash
# マージ中にコンフリクト発生
git merge feature-branch

# コンフリクトを確認
git status

# ファイルを編集してコンフリクトマーカーを削除
# <<<<<<<, =======, >>>>>>> を解決

# 解決済みとしてマーク
git add <resolved-file>

# マージを完了
git commit

# マージを中止する場合
git merge --abort
```

### 歴史の整理

```bash
# 直近3つのコミットをsquash
git rebase -i HEAD~3

# エディタで pick を squash に変更

# コミットメッセージを統合

# 強制プッシュ（注意！）
git push --force-with-lease
```

### スタッシュ

```bash
# 変更を一時保存
git stash

# メッセージ付き
git stash save "Work in progress on feature X"

# 一覧
git stash list

# 適用
git stash apply

# 適用して削除
git stash pop

# 削除
git stash drop stash@{0}
```

## トラブルシューティング

### 問題: 間違ったブランチにコミット

```bash
# 1. 現在のブランチ名を確認
git branch

# 2. コミットを取り消し（変更は保持）
git reset --soft HEAD~1

# 3. 正しいブランチに切り替え
git checkout correct-branch

# 4. 再度コミット
git add .
git commit -m "Your commit message"
```

### 問題: 機密情報をコミット

```bash
# 最新コミットの場合
git reset --soft HEAD~1
# ファイルを修正
git add .
git commit -m "Fixed commit"

# 既にプッシュ済みの場合
# 1. ファイルを履歴から削除
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret/file" \
  --prune-empty --tag-name-filter cat -- --all

# 2. 強制プッシュ
git push --force --all
```

### 問題: リベース失敗

```bash
# リベース中止
git rebase --abort

# または続行
git rebase --continue
```

## Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# ESLint実行
npm run lint || exit 1

# テスト実行
npm test || exit 1

# 機密情報チェック
if git diff --cached | grep -i "password\|secret\|api[_-]key"; then
  echo "機密情報が含まれている可能性があります"
  exit 1
fi

exit 0
```

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22

---

**使用例**:

```
以下の操作のGitコマンドを教えて：
1. 新しいブランチを作成
2. 変更をコミット
3. mainブランチの最新を取り込む
4. コンフリクトを解決
5. プッシュ
```

安全で正確なGitコマンドが生成されます！
