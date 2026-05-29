---
name: azure-boards-helper
description: Manage Azure Boards work items including user stories, tasks, and bugs with WIQL queries. Use when managing Azure Boards work items or creating sprint backlogs.
---

# Azure Boards Helper Skill

Azure Boardsでワークアイテムを管理するスキルです。

## 概要

Azure Boardsのワークアイテム作成、クエリ、レポート生成を支援します。

## 主な機能

- **ワークアイテム作成**: User Story、Task、Bug
- **クエリ作成**: WIQL (Work Item Query Language)
- **スプリント管理**: バックログ、スプリント計画
- **レポート**: バーンダウン、ベロシティ
- **自動化**: ワークフロー自動化

## ワークアイテムテンプレート

### User Story

```json
{
  "op": "add",
  "path": "/fields/System.Title",
  "value": "ユーザーログイン機能の実装"
},
{
  "op": "add",
  "path": "/fields/System.WorkItemType",
  "value": "User Story"
},
{
  "op": "add",
  "path": "/fields/System.Description",
  "value": "ユーザーがメールアドレスとパスワードでログインできるようにする"
},
{
  "op": "add",
  "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
  "value": "- メールアドレスとパスワードでログインできる\n- 無効な認証情報の場合エラーメッセージが表示される\n- ログイン成功後、ダッシュボードにリダイレクトされる"
},
{
  "op": "add",
  "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints",
  "value": 5
},
{
  "op": "add",
  "path": "/fields/System.State",
  "value": "New"
},
{
  "op": "add",
  "path": "/fields/System.AreaPath",
  "value": "MyProject\\Authentication"
},
{
  "op": "add",
  "path": "/fields/System.IterationPath",
  "value": "MyProject\\Sprint 1"
}
```

### Bug

```json
{
  "op": "add",
  "path": "/fields/System.Title",
  "value": "ログインボタンがクリックできない"
},
{
  "op": "add",
  "path": "/fields/System.WorkItemType",
  "value": "Bug"
},
{
  "op": "add",
  "path": "/fields/Microsoft.VSTS.TCM.ReproSteps",
  "value": "1. ログインページを開く\n2. メールアドレスとパスワードを入力\n3. ログインボタンをクリック\n\n期待: ログインされる\n実際: 何も起こらない"
},
{
  "op": "add",
  "path": "/fields/Microsoft.VSTS.Common.Severity",
  "value": "2 - High"
},
{
  "op": "add",
  "path": "/fields/Microsoft.VSTS.Common.Priority",
  "value": 1
}
```

## WIQLクエリ

### アクティブなUser Stories

```sql
SELECT
    [System.Id],
    [System.Title],
    [System.State],
    [Microsoft.VSTS.Scheduling.StoryPoints]
FROM WorkItems
WHERE
    [System.TeamProject] = @project
    AND [System.WorkItemType] = 'User Story'
    AND [System.State] <> 'Closed'
    AND [System.State] <> 'Removed'
ORDER BY [System.State] ASC, [Microsoft.VSTS.Common.Priority] ASC
```

### 今スプリントのタスク

```sql
SELECT
    [System.Id],
    [System.Title],
    [System.AssignedTo],
    [System.State],
    [Microsoft.VSTS.Scheduling.RemainingWork]
FROM WorkItems
WHERE
    [System.TeamProject] = @project
    AND [System.WorkItemType] = 'Task'
    AND [System.IterationPath] = @currentIteration
ORDER BY [System.State] ASC
```

### 未解決のバグ

```sql
SELECT
    [System.Id],
    [System.Title],
    [Microsoft.VSTS.Common.Severity],
    [Microsoft.VSTS.Common.Priority],
    [System.CreatedDate]
FROM WorkItems
WHERE
    [System.TeamProject] = @project
    AND [System.WorkItemType] = 'Bug'
    AND [System.State] <> 'Closed'
ORDER BY [Microsoft.VSTS.Common.Priority] ASC, [Microsoft.VSTS.Common.Severity] ASC
```

## Azure CLI コマンド

### ワークアイテム作成

```bash
# User Story作成
az boards work-item create \
  --title "新機能: ユーザープロフィール編集" \
  --type "User Story" \
  --description "ユーザーが自分のプロフィールを編集できるようにする" \
  --assigned-to "user@example.com" \
  --area "MyProject\\Features" \
  --iteration "MyProject\\Sprint 2" \
  --fields "Microsoft.VSTS.Scheduling.StoryPoints=3"

# Bug作成
az boards work-item create \
  --title "ログアウト後もセッションが残る" \
  --type "Bug" \
  --description "ログアウトボタンをクリックしてもセッションが破棄されない" \
  --fields "Microsoft.VSTS.Common.Severity=1 - Critical" "Microsoft.VSTS.Common.Priority=1"
```

### クエリ実行

```bash
# クエリ実行
az boards query \
  --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.WorkItemType] = 'Bug' AND [System.State] = 'Active'"

# 保存済みクエリ実行
az boards query --id "shared-queries/active-bugs"
```

## スプリント管理

### スプリント作成

```bash
# 新スプリント作成
az boards iteration project create \
  --name "Sprint 3" \
  --project "MyProject" \
  --start-date "2024-07-01" \
  --finish-date "2024-07-14"
```

### バックログの優先順位付け

```bash
# ワークアイテムの優先順位変更
az boards work-item update \
  --id 123 \
  --fields "Microsoft.VSTS.Common.Priority=1"
```

## REST API 使用例

### ワークアイテム作成（Python）

```python
import requests
import json

organization = "myorg"
project = "MyProject"
pat = "your-personal-access-token"

url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$User Story?api-version=7.0"

headers = {
    "Content-Type": "application/json-patch+json",
    "Authorization": f"Basic {pat}"
}

body = [
    {
        "op": "add",
        "path": "/fields/System.Title",
        "value": "新しいユーザーストーリー"
    },
    {
        "op": "add",
        "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints",
        "value": 5
    }
]

response = requests.post(url, headers=headers, data=json.dumps(body))
work_item = response.json()
print(f"Created work item: {work_item['id']}")
```

## レポート

### ベロシティレポート

```markdown
# Sprint Velocity Report

| Sprint   | Planned | Completed | Velocity |
|----------|---------|-----------|----------|
| Sprint 1 | 25      | 22        | 22       |
| Sprint 2 | 28      | 26        | 26       |
| Sprint 3 | 30      | 28        | 28       |
| Sprint 4 | 32      | 30        | 30       |

**平均ベロシティ**: 26.5 Story Points
**トレンド**: ↗️ 上昇傾向
```

### バーンダウンチャート

```
Sprint 2 Burndown

Story Points Remaining
30 |●
25 |  ●
20 |    ●●
15 |      ●●
10 |        ●●
5  |          ●●
0  |____________●●
   Day 1  5  10  14
```

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22
