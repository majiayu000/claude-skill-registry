---
name: github-issue-dependency
description: GitHub Issue間の依存関係（Is blocking / Blocked by）を設定・取得するためのAPI操作を提供
---

# GitHub Issue依存関係管理

> **参照元**: decompose-issue.md, subtask-detection.md から利用される依存関係管理スキル

---

## 概要

GitHub Issue間の「ブロック関係」を管理する機能。2025年8月にGA（一般提供）となった。

**用語**:
- `Is blocking`: このIssueが他のIssueの着手をブロックしている
- `Blocked by`: このIssueが他のIssueによってブロックされている

**Reference**: https://docs.github.com/en/rest/issues/issue-dependencies

---

## CLIスクリプト

**自動化スクリプトが利用可能です：**

```bash
# 依存関係を追加（#10 は #5 にブロックされている）
bash .opencode/skill/github-issue-dependency/scripts/issue-dependency.sh add-blocked-by 10 5

# 依存関係を削除
bash .opencode/skill/github-issue-dependency/scripts/issue-dependency.sh remove-blocked-by 10 5

# 依存関係を一覧表示
bash .opencode/skill/github-issue-dependency/scripts/issue-dependency.sh list 10
```

| コマンド | 引数 | 説明 |
|----------|------|------|
| `add-blocked-by` | `<issue> <blocking-issue>` | Issue が blocking-issue にブロックされていることを設定 |
| `remove-blocked-by` | `<issue> <blocking-issue>` | ブロック関係を削除 |
| `list` | `<issue>` | Issue の依存関係を一覧表示 |

---

## REST API

### 依存関係追加（Blocked by）

```bash
# 前提: Issue番号からdatabase IDを取得する必要がある

# 1. blocking Issue の database ID を取得
BLOCKING_ISSUE_ID=$(gh api "repos/{owner}/{repo}/issues/{blocking_number}" --jq '.id')

# 2. 依存関係を追加
gh api "repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by" \
  -X POST \
  -f "issue_id=${BLOCKING_ISSUE_ID}"
```

### 依存関係削除

```bash
# blocking Issue の database ID が必要
gh api "repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by/{blocking_issue_id}" \
  -X DELETE
```

### 依存関係取得

```bash
# このIssueをブロックしているIssue一覧
gh api "repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by" \
  --jq '.[] | {number, title, state}'

# このIssueがブロックしているIssue一覧
gh api "repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocking" \
  --jq '.[] | {number, title, state}'
```

---

## GraphQL API

REST APIの代わりにGraphQL APIも使用可能。Node IDを使用する。

### 依存関係追加

```bash
# 1. Node ID を取得
ISSUE_NODE_ID=$(gh issue view 10 --json id --jq '.id')
BLOCKING_NODE_ID=$(gh issue view 5 --json id --jq '.id')

# 2. 依存関係を追加
gh api graphql -f query='
  mutation($issueId: ID!, $blockingIssueId: ID!) {
    addBlockedBy(input: {
      issueId: $issueId,
      blockingIssueId: $blockingIssueId
    }) {
      issue {
        id
        number
        title
      }
    }
  }
' -f issueId="$ISSUE_NODE_ID" -f blockingIssueId="$BLOCKING_NODE_ID"
```

### 依存関係取得（GraphQL）

```bash
gh api graphql -f query='
  query($owner: String!, $name: String!, $number: Int!) {
    repository(owner: $owner, name: $name) {
      issue(number: $number) {
        id
        title
        blockedBy(first: 50) {
          nodes {
            number
            title
            state
          }
        }
        blocking(first: 50) {
          nodes {
            number
            title
            state
          }
        }
        issueDependenciesSummary {
          totalBlockedBy
          totalBlocking
        }
      }
    }
  }
' -f owner="OWNER" -f name="REPO" -F number=10
```

---

## 処理フロー（Subtask作成時）

```python
def add_subtask_dependencies(parent_id: int, subtask_ids: list[int], dependencies: dict[int, list[int]]) -> None:
    """
    Subtask作成後に依存関係を設定する
    
    Args:
        parent_id: 親Issue番号
        subtask_ids: 作成されたSubtaskのIssue番号リスト
        dependencies: {subtask_id: [depends_on_ids]} の依存関係マップ
    """
    for subtask_id, deps in dependencies.items():
        for dep_id in deps:
            if dep_id in subtask_ids:  # 同じ親の子Issue間のみ
                # subtask_id は dep_id にブロックされている
                bash(f'''
                    bash .opencode/skill/github-issue-dependency/scripts/issue-dependency.sh \
                      add-blocked-by {subtask_id} {dep_id}
                ''')
```

---

## エラーハンドリング

| エラー | 対応 |
|--------|------|
| Issue ID取得失敗 | 警告ログ出力してスキップ |
| API呼び出し失敗 | リトライ1回後スキップ（致命的エラーとしない） |
| 循環依存の検出 | API側でエラー → 警告表示してスキップ |
| 既に依存関係が存在 | 成功として扱う（冪等性） |

**重要**: 依存関係設定の失敗はワークフロー全体を停止させない。Issue自体は作成済みなので、手動で依存関係を設定可能。

---

## 使用箇所

| ワークフロー | 用途 |
|-------------|------|
| `/decompose-issue` | 分割したSubtask間の依存関係を設定 |
| `subtask-detection` | 依存関係を考慮した実行順序の決定 |
| `/detailed-design-workflow` | 作成したIssue間の依存関係を設定 |

---

## 制限事項

| 制限 | 値 |
|------|-----|
| 1 Issue あたりの最大依存関係数 | 50件（blocked by / blocking 各） |
| クロスリポジトリ | 非対応（同一リポジトリ内のみ） |

---

## 変更履歴

| 日付 | 変更内容 |
|------|---------|
| 2026-01-25 | 初版作成。REST API / GraphQL API両対応 |
