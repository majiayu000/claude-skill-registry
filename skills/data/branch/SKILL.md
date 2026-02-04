---
name: branch
description: gitブランチの作成・切り替え・一覧・削除を行う。「ブランチ作って」「ブランチ切り替えて」「ブランチ整理して」などのリクエストで使用する。
allowed-tools: Bash
argument-hint: [create|switch|list|delete] [ブランチ名]
---

# Git ブランチ管理

フィーチャーブランチの作成、切り替え、一覧表示、削除を行う。

## ブランチ命名規則

```
<type>/<短い説明（英語ケバブケース）>
```

### type 一覧

| type | 用途 | 例 |
|---|---|---|
| `feature` | 新機能開発 | `feature/auth-screen` |
| `fix` | バグ修正 | `fix/login-error` |
| `refactor` | リファクタリング | `refactor/hiroba-api` |
| `chore` | 設定・ツール変更 | `chore/update-deps` |
| `docs` | ドキュメント | `docs/api-guide` |
| `ui` | UI/デザイン変更 | `ui/home-screen-redesign` |

## 操作一覧

### ブランチ作成（create）

```bash
# 現在のブランチの最新状態から作成
git checkout -b <type>/<名前>

# リモートの main から作成（推奨）
git fetch origin && git checkout -b <type>/<名前> origin/main
```

### ブランチ切り替え（switch）

```bash
# ローカルブランチに切り替え
git switch <ブランチ名>

# 未コミットの変更がある場合は stash してから切り替え
git stash && git switch <ブランチ名>
```

### ブランチ一覧（list）

```bash
# ローカルブランチ一覧
git branch -v

# リモートを含む全ブランチ
git branch -av
```

### ブランチ削除（delete）

```bash
# マージ済みブランチを削除
git branch -d <ブランチ名>

# リモートブランチも削除
git push origin --delete <ブランチ名>
```

## 手順

1. 引数から操作タイプ（create / switch / list / delete）を判定する
2. 引数にブランチ名やキーワードがあれば命名規則に従ってブランチ名を生成する
3. `git status` で未コミットの変更がないか確認する
4. 未コミットの変更がある場合はユーザーに対応方法を確認する（コミット / stash / 破棄）
5. 操作を実行する

## ルール

- `main` ブランチへの直接コミットは推奨しない。作業はフィーチャーブランチで行う
- ブランチ作成時は `origin/main` の最新を取得してから分岐する
- ブランチ削除前にマージ状態を確認する
- `git branch -D`（強制削除）は明示的に指示された場合のみ使用する
- ブランチ名は英語のケバブケースで統一する
- 切り替え前に未コミットの変更を必ず確認する
