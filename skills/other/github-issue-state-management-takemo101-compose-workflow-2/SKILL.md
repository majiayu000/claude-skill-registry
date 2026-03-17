---
name: github-issue-state-management
description: GitHub Issueのラベルとメタデータを使用した環境状態管理。container-use/worktree/ホスト環境すべてからアクセス可能なSingle Source of Truth
---

# GitHub Issue 状態管理

> **Single Source of Truth**: GitHub Issue のラベルとメタデータによる環境状態管理

---

## 概要

**なぜ GitHub Issue で管理するのか？**

| 課題（ローカルファイル） | 解決策（GitHub Issue） |
|--------------------------|----------------------|
| container-use内からホストファイルにアクセス不可 | `gh` CLI はどこからでも使用可能 |
| worktree間でファイル共有不可 | Issue は全環境で同一 |
| 並列実行時の競合リスク | ラベル操作は GitHub がアトミック処理 |
| ローカルファイルのため可視性が低い | GitHub UI で状態が一目瞭然 |

---

## ラベル体系

### ステータスラベル（排他: 1つのみ）

| ラベル | 説明 | 色（推奨） |
|--------|------|----------|
| `env:active` | 作業中 | `#0E8A16` (緑) |
| `env:blocked` | **人間の介入が必要** | `#D93F0B` (赤) |
| `env:pr-created` | PR作成済み | `#1D76DB` (青) |
| `env:merged` | マージ完了 | `#6F42C1` (紫) |

### Phase ラベル（排他: 1つのみ）

| ラベル | 説明 |
|--------|------|
| `phase:0-branch` | ブランチ作成 |
| `phase:1-env` | 環境構築 |
| `phase:2-design` | 設計書参照 |
| `phase:3-check` | 設計書実現性チェック |
| `phase:4-red` | テスト作成（Red） |
| `phase:5-green` | 実装（Green） |
| `phase:6-refactor` | リファクタリング |
| `phase:7-review` | レビュー依頼/修正 |
| `phase:8-stress` | ストレステスト（任意） |
| `phase:9-approval` | ユーザー承認待ち |
| `phase:10-pr` | PR作成 |
| `phase:11-ci` | CI監視 |
| `phase:12-merge` | マージ & クリーンアップ |

### 領域ラベル（任意: 複数可）

| ラベル | 説明 |
|--------|------|
| `area:backend` | バックエンド |
| `area:frontend` | フロントエンド |
| `area:infra` | インフラ |
| `area:database` | データベース |

---

## メタデータ管理

### Issue Body へのメタデータ埋め込み

Issue 作成時または環境開始時に、Issue body の**末尾**に以下のブロックを追加：

```markdown
<!-- ENV_METADATA
env_id: abc-123-def
branch: feature/issue-42-user-auth
env_type: container-use
worktree_path: 
created_at: 2026-01-17T10:00:00Z
last_updated_at: 2026-01-17T15:30:00Z
-->
```

### フィールド定義

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `env_id` | string | ✅ | container-use 環境ID または worktree 識別子 |
| `branch` | string | ✅ | Git ブランチ名 |
| `env_type` | string | ✅ | `container-use` / `worktree` / `host` |
| `worktree_path` | string | | worktree 使用時のパス |
| `pr_number` | string | | PR作成後に設定（途中再開時のCI監視に必要） |
| `created_at` | string | ✅ | 作成日時（ISO 8601） |
| `last_updated_at` | string | ✅ | 最終更新日時（ISO 8601） |

### メタデータの抽出

```bash
# Issue body からメタデータを抽出
gh issue view 42 --json body -q '.body' | \
  grep -oP '(?<=<!-- ENV_METADATA)[\s\S]*?(?=-->)' | \
  grep -E '^[a-z_]+:' | \
  sed 's/^/  /'
```

---

## Blocked 状態の詳細記録

### Blocked コメント形式

Blocked 発生時は、ラベル変更と共に以下形式のコメントを追加：

```markdown
## Blocked: [reason_code]

**Description**: [問題の詳細説明]

**Suggested Action**: [推奨される解決アクション]

**Context**:
- [関連情報1]
- [関連情報2]

**Blocked at**: 2026-01-17T14:00:00Z

---
> このコメントは `env:blocked` ラベルと連動しています。
> 問題解決後、ラベルを `env:active` に変更し、このコメントに「Resolved」と返信してください。
```

### Blocked Reason コード

| Reason | 説明 | 推奨アクション |
|--------|------|---------------|
| `design_ambiguity` | 設計書実現性チェックNG | 設計書修正 |
| `review_loop_exceeded` | レビュー3回失敗 | 設計書見直し |
| `dependency_missing` | 依存Subtask未完了 | 依存解決待ち |
| `external_blocker` | 外部要因（API未提供等） | 人間エスカレーション |
| `resource_limit` | 環境リソース不足 | Docker cleanup |
| `ci_persistent_failure` | CI 3回連続失敗 | 手動調査必要 |

---

## API 操作

### 主要関数（CLI ラッパー）

| 関数 | 用途 | コマンド例 |
|------|------|----------|
| `register_env` | 環境開始時に登録 | `issue-state.sh register 42 abc-123 feature/auth container-use` |
| `update_phase` | Phase更新 | `issue-state.sh phase 42 5-green` |
| `set_blocked` | Blocked状態に設定 | `issue-state.sh block 42 design_ambiguity "設計に矛盾"` |
| `clear_blocked` | Blocked解除 | `issue-state.sh unblock 42` |
| `get_state` | 現在の状態取得 | `issue-state.sh get 42` |
| `list_active` | アクティブな環境一覧 | `issue-state.sh list` |

### 直接 gh コマンド

```bash
# 環境登録（ラベル追加）
gh issue edit 42 --add-label "env:active,phase:1-env,area:backend"

# Phase 更新（ラベル入れ替え）
gh issue edit 42 --remove-label "phase:4-red" --add-label "phase:5-green"

# Blocked 設定
gh issue edit 42 --remove-label "env:active" --add-label "env:blocked"
gh issue comment 42 --body "## Blocked: design_ambiguity..."

# PR作成済みに更新
gh issue edit 42 --remove-label "env:active" --add-label "env:pr-created"

# 状態取得（JSON）
gh issue view 42 --json number,title,labels,body,comments

# アクティブな環境一覧
gh issue list --label "env:active" --json number,title,labels

# Blocked な環境一覧
gh issue list --label "env:blocked" --json number,title,labels
```

---

## 必須更新ポイント (NON-NEGOTIABLE)

| トリガー | アクション | ラベル操作 |
|---------|----------|----------|
| 環境作成開始 | ラベル追加 + メタデータ埋め込み | `+env:active`, `+phase:1-env` |
| Phase 遷移 | ラベル入れ替え | `-phase:X`, `+phase:Y` |
| Blocked 発生 | ラベル変更 + コメント追加 | `-env:active`, `+env:blocked` |
| Blocked 解除 | ラベル変更 | `-env:blocked`, `+env:active` |
| PR 作成 | ラベル変更 | `-env:active`, `+env:pr-created`, `+phase:10-pr` |
| PR マージ | ラベル変更 | `-env:pr-created`, `+env:merged`, `+phase:12-merge` |
| 環境削除 | ラベル削除 | 全 `env:*`, `phase:*` ラベルを削除 |

---

## セッション復旧（途中再開）

### resume コマンド（推奨）

```bash
# 復旧情報をJSON形式で取得
bash .opencode/skill/github-issue-state-management/scripts/issue-state.sh resume 42
```

**出力例**:
```json
{
  "issue_number": 42,
  "status": "env:active",
  "phase": "5-green",
  "env_id": "abc-123-def",
  "branch": "feature/issue-42-user-auth",
  "env_type": "container-use",
  "action": "reopen_environment",
  "command": "environment_open with env_id=abc-123-def"
}
```

### 復旧判定マトリクス

| ステータス | Phase | アクション | 具体的な操作 |
|-----------|-------|----------|-------------|
| `env:active` | `0-branch` | 環境作成 | `environment_create(from_git_ref=branch)` |
| `env:active` | `1-env`〜`6-refactor` | 環境再開 | `environment_open(env_id=...)` |
| `env:active` | `7-review`〜`8-stress` | レビュー再開 | 環境を開いてレビューループを継続 |
| `env:active` | `9-approval` | 承認待ち | ユーザーに承認ゲートを提示 |
| `env:active` | `10-pr`〜`11-ci` | CI監視 | `gh pr checks <pr_number>` |
| `env:blocked` | - | **人間の介入** | Blockedコメント確認 → 解決 → `unblock` |
| `env:pr-created` | - | PR確認 | `gh pr view` で状態確認 |
| `env:merged` | - | クリーンアップ | 環境削除（残っている場合） |
| (なし) | - | 初期化 | `register` で環境を登録 |

### 手動復旧手順（参考）

```bash
# 1. アクティブな環境を検索
gh issue list --label "env:active" --json number,title,labels

# 2. 特定 Issue の復旧情報を取得
bash .opencode/skill/github-issue-state-management/scripts/issue-state.sh resume 42

# 3. 出力された action/command に従って再開
```

---

## 並列実行時のルール

| Actor | 責任 |
|-------|------|
| `container-worker` | 作業完了後、自身で `phase` ラベルを更新可能 |
| Main agent (Sisyphus) | 複数 Issue を並列処理する場合、各 Issue を独立して管理 |

**競合回避**:
- 同一 Issue への同時編集は避ける（既存ルールと同じ）
- ラベル操作は GitHub がアトミックに処理するため、ファイルベースより安全

---

## ラベル初期設定

リポジトリに必要なラベルを一括作成：

```bash
# ステータスラベル
gh label create "env:active" --color "0E8A16" --description "作業中"
gh label create "env:blocked" --color "D93F0B" --description "人間の介入が必要"
gh label create "env:pr-created" --color "1D76DB" --description "PR作成済み"
gh label create "env:merged" --color "6F42C1" --description "マージ完了"

# Phase ラベル
gh label create "phase:0-branch" --color "FBCA04" --description "ブランチ作成"
gh label create "phase:1-env" --color "FBCA04" --description "環境構築"
gh label create "phase:2-design" --color "FBCA04" --description "設計書参照"
gh label create "phase:3-check" --color "FBCA04" --description "設計実現性チェック"
gh label create "phase:4-red" --color "FBCA04" --description "TDD Red"
gh label create "phase:5-green" --color "FBCA04" --description "TDD Green"
gh label create "phase:6-refactor" --color "FBCA04" --description "リファクタリング"
gh label create "phase:7-review" --color "FBCA04" --description "レビュー"
gh label create "phase:8-stress" --color "FBCA04" --description "ストレステスト"
gh label create "phase:9-approval" --color "FBCA04" --description "承認待ち"
gh label create "phase:10-pr" --color "FBCA04" --description "PR作成"
gh label create "phase:11-ci" --color "FBCA04" --description "CI監視"
gh label create "phase:12-merge" --color "FBCA04" --description "マージ完了"

# 領域ラベル
gh label create "area:backend" --color "C2E0C6" --description "バックエンド"
gh label create "area:frontend" --color "C2E0C6" --description "フロントエンド"
gh label create "area:infra" --color "C2E0C6" --description "インフラ"
gh label create "area:database" --color "C2E0C6" --description "データベース"
```

---

## CLI スクリプト

**使用方法**:

```bash
bash .opencode/skill/github-issue-state-management/scripts/issue-state.sh <command> [args...]
```

| コマンド | 説明 | 使用例 |
|----------|------|--------|
| `register` | 環境を登録 | `issue-state.sh register 42 abc-123 feature/auth container-use` |
| `phase` | Phase を更新 | `issue-state.sh phase 42 5-green` |
| `block` | Blocked 状態に設定 | `issue-state.sh block 42 design_ambiguity "説明"` |
| `unblock` | Blocked を解除 | `issue-state.sh unblock 42` |
| `pr-created` | PR作成済みに更新 | `issue-state.sh pr-created 42 25` |
| `merged` | マージ完了に更新 | `issue-state.sh merged 42` |
| `get` | 状態を取得 | `issue-state.sh get 42` |
| `list` | アクティブ一覧 | `issue-state.sh list` |
| `resume` | **途中再開情報を取得** | `issue-state.sh resume 42` |
| `init-labels` | ラベル一括作成 | `issue-state.sh init-labels` |

### エラーリトライ

スクリプトはネットワークエラーやGitHub APIのレート制限に対して自動リトライを行います。

| 設定 | 環境変数 | デフォルト |
|------|---------|-----------|
| 最大リトライ回数 | `MAX_RETRIES` | 3 |
| リトライ間隔（秒） | `RETRY_DELAY` | 5 |

**レート制限時**: 60秒待機後にリトライ
**ネットワークエラー時**: `RETRY_DELAY`秒待機後にリトライ

```bash
# カスタムリトライ設定
MAX_RETRIES=5 RETRY_DELAY=10 bash issue-state.sh phase 42 5-green
```

---

## ハードブロック (違反禁止)

| 違反 | 結果 |
|------|------|
| 環境開始時にラベル未追加 | **FORBIDDEN** - 復旧不可 |
| Phase 遷移時にラベル未更新 | **FORBIDDEN** - 状態不整合 |
| Blocked 時にコメント未追加 | **FORBIDDEN** - 理由が不明 |

---

## 変更履歴

| 日付 | バージョン | 変更内容 |
|:---|:---|:---|
| 2026-01-17 | 1.0.0 | 初版作成 |
