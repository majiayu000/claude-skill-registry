---
name: repo-manager
description: |
  ユーザーからのリクエストをタスク分割して Issue 登録・プロジェクト管理・進捗報告。
  トリガー例: 「タスク管理」「実行して」「repo-manager」「これやって」「作って」
allowed-tools: Bash, Glob, Grep, Read, AskUserQuestion
arguments: auto-detect
user-invocable: true
---

# Repo Manager

ユーザーからのリクエストをタスク分割して Issue 登録・プロジェクト管理・進捗報告します。

## 前提条件

- GitHub CLI (`gh`) がインストール済み
- `gh auth login` で認証済み
- Agent-ZERO プロジェクト（ID: 11）が存在

## 除外条件

**プライベートリポジトリの場合は、このフローを実行しません。**

```bash
# リポジトリの可視性を確認
gh repo view --json visibility,owner,name
# visibility: "PRIVATE" の場合はスキップ
```

## ワークフロー

### 1. リクエスト解析

ユーザーからのリクエスト（`$ARGUMENTS`）を解析:

- リポジトリが指定されているか？
- ターゲットリポジトリは存在するか？
- プライベートリポジトリでないか？

### 2. リポジトリの決定

```bash
# リポジトリが指定されている場合
gh repo view OWNER/REPO

# リポジトリが指定されていない場合、またはリポジトリが存在しない場合
# → ZERO-CC リポジトリ (Sunwood-ai-labs/zero-cc) を使用
```

### 3. タスク分割

リクエストを具体的なタスクに分割:

1. **大まかなタスクを抽出**: リクエストの目的を達成するための主要なステップ
2. **各タスクを詳細化**: それぞれのタスクをさらに小さなサブタスクに
3. **優先順位付け**: 依存関係を考慮して順序を決定

### 4. Issue 作成

分割したタスクごとに Issue を作成:

```bash
gh issue create \
  --title "タスクのタイトル" \
  --body "## 概要\n\n詳細説明\n\n## タスク\n\n- [ ] サブタスク1\n- [ ] サブタスク2" \
  --label "enhancement"
```

### 5. プロジェクトへの追加

作成した Issue を Agent-ZERO プロジェクトに追加:

```bash
# プロジェクト ID: 11
gh project item-add 11 --url "IssueのURL" --owner Sunwood-ai-labs
```

### 6. 初期ステータス設定

Issue のステータスを「Todo」または「In Progress」に設定:

```bash
# ステータス変更（GraphQL でオプション ID を取得）
gh project item-edit \
  --project-id PVT_kwHOBnsxLs4BMiC9 \
  --id ITEM_ID \
  --field-id PVTSSF_lAHOBnsxLs4BMiC9zg7yZ1U \
  --single-select-option-id f75ad846  # Todo
```

### 7. 進捗報告

タスク実行中は以下の報告を行います:

1. **作業開始時**: ステータスを「In Progress」に変更
2. **サブタスク完了時**: Issue コメントで進捗を報告
3. **タスク完了時**: ステータスを「Done」に変更

```bash
# Issue コメントで進捗報告
gh issue comment ISSUE番号 --body "## 進捗\n\n- [x] サブタスク1 を完了"

# ステータスを Done に変更
gh project item-edit \
  --project-id PVT_kwHOBnsxLs4BMiC9 \
  --id ITEM_ID \
  --field-id PVTSSF_lAHOBnsxLs4BMiC9zg7yZ1U \
  --single-select-option-id 98236657  # Done
```

### 8. 日付設定

**重要: Issue をプロジェクトに追加した後、開始日と終了日を設定してください。**

```bash
# 1. フィールド一覧を取得（日付フィールドのIDを確認）
gh project field-list 11 --owner Sunwood-ai-labs

# 出力例:
# 開始日    ProjectV2Field    PVTF_lAHOBnsxLs4BMiC9zg71LEA
# 終了日    ProjectV2Field    PVTF_lAHOBnsxLs4BMiC9zg71LFU

# 2. アイテムIDを取得（GraphQLまたは既知のIDを使用）
# GraphQLで取得する場合:
gh api graphql --field query='
query($project: ID!) {
  repository(owner: "Sunwood-ai-labs", name: "zero-cc") {
    issue(number: ISSUE番号) {
      projectItems(first: 10) {
        nodes {
          id
        }
      }
    }
  }
}
' --field project=PVT_kwHOBnsxLs4BMiC9

# 3. 開始日を設定
gh project item-edit \
  --project-id PVT_kwHOBnsxLs4BMiC9 \
  --id ITEM_ID \
  --field-id PVTF_lAHOBnsxLs4BMiC9zg71LEA \
  --date "YYYY-MM-DD"

# 4. 終了日を設定
gh project item-edit \
  --project-id PVT_kwHOBnsxLs4BMiC9 \
  --id ITEM_ID \
  --field-id PVTF_lAHOBnsxLs4BMiC9zg71LFU \
  --date "YYYY-MM-DD"
```

**既知のID（Agent-ZERO プロジェクト）:**
- プロジェクトID: `PVT_kwHOBnsxLs4BMiC9`
- ステータスフィールドID: `PVTSSF_lAHOBnsxLs4BMiC9zg7yZ1U`
- 開始日フィールドID: `PVTF_lAHOBnsxLs4BMiC9zg71LEA`
- 終了日フィールドID: `PVTF_lAHOBnsxLs4BMiC9zg71LFU`
- Todo: `f75ad846`
- In Progress: `47fc9ee4`
- Done: `98236657`

## Issue テンプレート

```markdown
## 概要

[タスクの概要説明]

## 背景・目的

[なぜこのタスクが必要なのか]

## タスク

- [ ] サブタスク1
- [ ] サブタスク2
- [ ] サブタスク3

## 受入条件

- [ ] 条件1
- [ ] 条件2

## 関連リンク

- 関連 Issue: #
- 関連 PR: #
- ドキュメント:
```

## ステータス遷移

```
Todo → In Progress → Done
  ↑         │
  └─────────┘
      (中断時)
```

## 使用例

### 基本的な使用例

```
ユーザー: 「GitHub Actions のワークフローを設定して」

スキル:
1. タスク分割:
   - Issue 1: GitHub Actions の基本設定
   - Issue 2: CI/CD パイプラインの構築
   - Issue 3: テスト自動化の追加

2. Issue 作成 & プロジェクト追加

3. ステータス設定（Todo or In Progress）

4. 日付設定（開始日・終了日）

5. 進捗管理開始
```

### リポジトリが存在しない場合

```
ユーザー: 「新しいプロジェクトで Next.js のブログを作って」

スキル:
1. リポジトリが存在しないことを確認
2. ZERO-CC リポジトリに Issue を作成
3. タイトル: "[新プロジェクト] Next.js ブログの作成"
```

## 注意点

1. **プライベートリポジトリ**: このフローを実行せず、通常の開発モードで作業
2. **リポジトリ不存在**: ZERO-CC リポジトリをフォールバック先として使用
3. **タスク粒度**: Issue は 1-2 日で完了できる粒度に分割
4. **進捗報告**: 適宜 Issue コメントで進捗を報告
5. **日付設定**: Issue 作成後、必ず開始日と終了日を設定すること（YYYY-MM-DD形式）

## 参照

GitHub プロジェクト管理のコマンド詳細は **`project-mgmt`** スキルを参照してください:

- [.claude/skills/project-mgmt/SKILL.md](../project-mgmt/SKILL.md) - プロジェクト管理スキル
- [.claude/skills/project-mgmt/references/COMMANDS.md](../project-mgmt/references/COMMANDS.md) - コマンド詳細
- [.claude/skills/project-mgmt/references/EXAMPLES.md](../project-mgmt/references/EXAMPLES.md) - 使用例

**`repo-manager` は `project-mgmt` の機能を利用してタスク分割・進捗管理を行います。**
