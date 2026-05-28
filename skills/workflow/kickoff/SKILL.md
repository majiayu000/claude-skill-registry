---
name: kickoff
description: 作業開始。変更内容からブランチを作成し、初期コミットまで行う。
model: claude-sonnet-4-5-20250929
allowed-tools: Bash, Read, Glob, Grep
---

# Kickoff

変更内容を分析してブランチを作成し、初期コミットまで行います。

## Phase 1: 状態確認

以下を並列実行:

```bash
git branch --show-current
git status
git diff
git diff --cached
```

**前提条件:**
- 現在のブランチが `main` / `master` / `develop` であること
- 変更（unstaged または staged）が存在すること

**条件を満たさない場合:**
- feature branch にいる → 「既に feature branch です。/commit を使用してください」で終了
- 変更がない → 「コミットする変更がありません」で終了

## Phase 2: ブランチ作成

### 2-1. 変更内容の分析

1. diff の内容を分析
2. 主要な変更ファイルを Read で確認
3. 変更の目的・性質を特定

### 2-2. ブランチ名の生成

**命名規則:**
```
<prefix>/<summary>
```

| prefix | 用途 |
|--------|------|
| feat/ | 新機能 |
| fix/ | バグ修正 |
| refactor/ | リファクタリング |
| docs/ | ドキュメント |
| chore/ | 設定変更、依存関係更新等 |

- summary: kebab-case、英語、20文字以内目安
- 例: `feat/add-logout-button`, `fix/login-validation`

### 2-3. ブランチ作成

```bash
git checkout -b <ブランチ名>
```

## Phase 3: 初期コミット

### 3-1. ステージング

```bash
git add <files>
```

**除外対象:**
- シークレット（.env, credentials.json 等）
- 一時ファイル（*.log, *.tmp 等）

### 3-2. コミット

**メッセージ要件:**
- 変更の「why」に焦点（1〜2文）
- リポジトリの既存スタイルに準拠

```bash
git commit -m "$(cat <<'EOF'
<prefix>: <簡潔な説明>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet <noreply@anthropic.com>
EOF
)"
```

### 3-3. 確認

```bash
git status
git log -1 --stat
```

## 完了報告

- 作成したブランチ名
- コミットメッセージ
- 変更ファイル数
- 推奨する次のアクション（実装継続 / /ship でPR作成）
