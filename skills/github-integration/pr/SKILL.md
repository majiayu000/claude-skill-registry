---
name: pr
description: GitHub Pull Requestの作成・確認を行う。「PR作って」「プルリク作成」「PRの状態確認」などのリクエストで使用する。
allowed-tools: Read, Bash, Glob, Grep
argument-hint: [create|status|list] [タイトル（省略可）]
---

# GitHub Pull Request 管理

gh CLI を使用して Pull Request の作成と管理を行う。

## 前提条件

- `gh` CLI がインストール済みであること
- GitHub に認証済みであること（`gh auth status` で確認）

## 操作一覧

### PR 作成（create）

```bash
# 1. リモートにプッシュ
git push -u origin <現在のブランチ名>

# 2. PR 作成
gh pr create --title "<タイトル>" --body "$(cat <<'EOF'
## 概要
<変更内容の要約（箇条書き）>

## 変更種別
- [ ] 新機能 (feat)
- [ ] バグ修正 (fix)
- [ ] リファクタリング (refactor)
- [ ] UI/デザイン (ui)
- [ ] ドキュメント (docs)
- [ ] その他 (chore)

## スクリーンショット
（UI変更がある場合）

## テスト方法
<確認手順>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### PR 状態確認（status）

```bash
# 自分のPR一覧
gh pr status

# 特定PRの詳細
gh pr view <PR番号>

# PRのチェック状態
gh pr checks <PR番号>
```

### PR 一覧（list）

```bash
# オープン中のPR一覧
gh pr list

# 全状態のPR一覧
gh pr list --state all --limit 10
```

## 手順

### PR 作成時

1. `gh auth status` で GitHub 認証を確認する
2. `git status` で未コミットの変更がないか確認する（あればコミットを促す）
3. `git log main..HEAD --oneline` で現在のブランチのコミット一覧を取得する
4. `git diff main...HEAD --stat` で変更ファイルの統計を取得する
5. コミット内容と差分から PR タイトルと本文を生成する
6. ユーザーに PR 内容を提示し、確認を取る
7. リモートにプッシュし、PR を作成する
8. 作成された PR の URL を報告する

### PR 確認時

1. `gh pr status` または `gh pr list` で状態を取得する
2. 結果をわかりやすく整形して報告する

## PR タイトル規約

コミットメッセージと同じ Conventional Commits 形式を使用する:

```
<type>: <日本語で簡潔な説明>
```

例:
- `feat: 認証画面を実装`
- `fix: ログイン時のエラーハンドリングを修正`
- `ui: ホーム画面のレイアウトを調整`

## ルール

- `main` ブランチから直接 PR は作成しない（フィーチャーブランチが必要）
- PR 作成前に未コミットの変更がないことを確認する
- PR タイトルは日本語で、内容が一目でわかるようにする
- PR 本文には変更の概要と確認方法を含める
- `--force` プッシュは使用しない
