---
name: project-mgmt
description: |
  GitHub プロジェクト管理を一括操作。Issue作成、ラベル設定、プロジェクト紐付け、マイルストーン、日付、ステータス変更。
  トリガー例: 「Issue作成」「プロジェクト管理」「project-mgmt」「Issueを立てて」「プロジェクトに追加」
allowed-tools: Bash, Glob, Grep, Read, jq
arguments: auto-detect
user-invocable: true
---

# GitHub Project Manager

GitHub プロジェクト管理を一括操作します。

## 前提条件

- GitHub CLI (`gh`) がインストール済み
- `gh auth login` で認証済み
- `jq` がインストール済み（JSON パース用）
- 対象のプロジェクトが作成されている

## ID の動的取得

プロジェクトID、グローバルID、フィールドID、オプションID は動的に取得します。

```bash
# 変数設定
OWNER="Sunwood-ai-labs"
PROJECT_NAME="Agent-ZERO"

# プロジェクトIDの取得（ローカルID: 数字）
PROJECT_ID=$(gh project list --owner $OWNER --format json | jq -r ".[] | select(.title == \"$PROJECT_NAME\") | .number")

# プロジェクトグローバルIDの取得
PROJECT_GLOBAL_ID=$(gh project view $PROJECT_ID --owner $OWNER --format json | jq -r ".id")

# フィールドIDの取得（例: 開始日フィールド）
START_DATE_FIELD_ID=$(gh project field-list $PROJECT_ID --owner $OWNER | grep "開始日" | awk '{print $3}')

# アイテムIDの取得（Issue番号から）
ITEM_ID=$(gh project item-list $PROJECT_ID --owner $OWNER --format json | jq -r ".[] | select(.content.number == 7) | .id")

# ステータスフィールドとオプションIDの取得（GraphQL）
STATUS_INFO=$(gh api graphql -f query="
query {
  node(id: \"$PROJECT_GLOBAL_ID\") {
    ... on ProjectV2 {
      fields(first: 20) {
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
            options {
              id
              name
            }
          }
        }
      }
    }
  }
}")

STATUS_FIELD_ID=$(echo "$STATUS_INFO" | jq -r '.data.node.fields.nodes[] | select(.name == "Status") | .id')
TODO_OPTION_ID=$(echo "$STATUS_INFO" | jq -r '.data.node.fields.nodes[] | select(.name == "Status") | .options[] | select(.name == "Todo") | .id')
IN_PROGRESS_OPTION_ID=$(echo "$STATUS_INFO" | jq -r '.data.node.fields.nodes[] | select(.name == "Status") | .options[] | select(.name == "In Progress") | .id')
DONE_OPTION_ID=$(echo "$STATUS_INFO" | jq -r '.data.node.fields.nodes[] | select(.name == "Status") | .options[] | select(.name == "Done") | .id')
```

## ワークフロー

### 1. 引数解析
`$ARGUMENTS` から操作を特定:

- `issue-create` / `issue` → Issue 作成
- `label-create` / `label` → ラベル作成
- `project-add` → プロジェクトに紐付け
- `milestone-create` / `milestone` → マイルストーン作成・紐付け
- `set-date` / `date` → 日付設定（開始日・終了日）
- `set-status` / `status` → ステータス変更

### 2. Issue 作成

```bash
# 基本形
gh issue create --title "タイトル" --body "本文" --label "label1,label2"

# 例
gh issue create --title "テスト Issue" --body "## 概要\n\n詳細をここに書く" --label "enhancement"
```

### 3. ラベル作成・追加

```bash
# ラベル作成
gh label create ラベル名 --color "#カラー" --description "説明"

# ラベル一覧
gh label list

# Issue にラベル追加
gh issue edit ISSUE番号 --add-label "label1,label2"
```

### 4. プロジェクトに紐付け

```bash
# プロジェクト一覧
gh project list --owner OWNER

# プロジェクト詳細（グローバルID取得）
gh project view PROJECT番号 --owner OWNER --format json

# Item 追加
gh project item-add PROJECT番号 --url "https://github.com/OWNER/REPO/issues/ISSUE番号" --owner OWNER
```

### 5. マイルストーン作成・紐付け

```bash
# マイルストーン作成（gh api 使用）
gh api --method POST /repos/OWNER/REPO/milestones -f title="v0.1.0" -f description="説明"

# Issue にマイルストーン紐付け
gh api --method PATCH /repos/OWNER/REPO/issues/ISSUE番号 -f milestone=MILESTONE_ID

# マイルストーン一覧
gh api /repos/OWNER/REPO/milestones
```

### 6. 日付設定（開始日・終了日）

```bash
# 日付フィールド作成
gh project field-create $PROJECT_ID --owner $OWNER --name "開始日" --data-type DATE
gh project field-create $PROJECT_ID --owner $OWNER --name "終了日" --data-type DATE

# フィールドIDを取得
START_DATE_FIELD_ID=$(gh project field-list $PROJECT_ID --owner $OWNER | grep "開始日" | awk '{print $3}')
END_DATE_FIELD_ID=$(gh project field-list $PROJECT_ID --owner $OWNER | grep "終了日" | awk '{print $3}')

# 日付設定（変数を使用）
gh project item-edit --project-id $PROJECT_GLOBAL_ID --id $ITEM_ID --field-id $START_DATE_FIELD_ID --date "YYYY-MM-DD"
gh project item-edit --project-id $PROJECT_GLOBAL_ID --id $ITEM_ID --field-id $END_DATE_FIELD_ID --date "YYYY-MM-DD"
```

### 7. ステータス変更

```bash
# ステータス変更（変数を使用）
gh project item-edit --project-id $PROJECT_GLOBAL_ID --id $ITEM_ID --field-id $STATUS_FIELD_ID --single-select-option-id $IN_PROGRESS_OPTION_ID
```

## 使用例

### Issue 一括作成とプロジェクト登録

```bash
/project-mgmt issue-create "機能改善" "enhancement,test"
```

### マイルストーン付き Issue 作成

```bash
/project-mgmt milestone-create v0.1.0 "MVP リリース"
```

### ステータス変更

```bash
/project-mgmt set-status 7 "In Progress"
/project-mgmt set-status 7 "Done"
```

### 日付設定

```bash
/project-mgmt set-date 7 "2026-01-15" "2026-01-20"
```

## 参考情報

- **Issue 作成**: `gh issue create --help`
- **ラベル**: `gh label create --help`
- **プロジェクト**: `gh project --help`
- **マイルストーン**: GitHub REST API 使用
- **日付**: プロジェクトに DATE フィールドを作成
- **ステータス**: GraphQL でオプションIDを取得

## 注意点

1. **ID の動的取得**: すべての ID は動的に取得します
   - プロジェクトID: `gh project list --format json | jq` で取得
   - プロジェクトグローバルID: `gh project view --format json | jq` で取得
   - フィールドID: `gh project field-list` で取得
   - アイテムID: `gh project item-list --format json | jq` で取得
   - ステータスオプションID: GraphQL + jq で取得

2. **jq の使用**: JSON パースには必ず `jq` を使用します
   - `grep` や `awk` での JSON パースは避けてください

3. **変数の使用**: コマンド例では変数（`$PROJECT_ID` など）を使用します
