---
name: github-graphql-api
description: GitHub REST APIのSub-issue関連バグを回避するためのGraphQL API共通処理（Sub-issue登録、エラーハンドリング）を提供
---

# GitHub GraphQL API共通処理

> **参照元**: decompose-issue.md, detailed-design-workflow.md から分離された共通GraphQL API処理

---

## 概要

GitHub REST APIにはSub-issue関連のバグがあるため、GraphQL APIを使用する。

**Reference**: https://github.com/cli/cli/issues/10378

---

## Sub-issue登録

親IssueにSub-issueを紐付けるGraphQL API処理。

### 処理フロー

```python
def add_sub_issue(parent_issue_id: int, child_issue_id: int) -> bool:
    """
    親IssueにSub-issueを登録する
    
    Args:
        parent_issue_id: 親Issue番号
        child_issue_id: 子Issue番号（Sub-issue）
    
    Returns:
        成功時True、失敗時False（致命的エラーとしない）
    """
    try:
        # 1. GraphQL Node IDを取得
        parent_node_id = bash(
            f"gh issue view {parent_issue_id} --json id --jq '.id'"
        ).stdout.strip()
        
        child_node_id = bash(
            f"gh issue view {child_issue_id} --json id --jq '.id'"
        ).stdout.strip()
        
        if not parent_node_id or not child_node_id:
            return False
        
        # 2. GraphQL APIでSub-issue関係を追加
        result = bash(f'''
            gh api graphql \
              -H "GraphQL-Features: sub_issues" \
              -f 'query=mutation {{
                addSubIssue(input: {{
                  issueId: "{parent_node_id}",
                  subIssueId: "{child_node_id}"
                }}) {{
                  issue {{ number }}
                  subIssue {{ number }}
                }}
              }}'
        ''')
        
        return result.exit_code == 0
        
    except Exception:
        return False  # Sub-issue登録失敗は致命的エラーとしない
```

### シェルコマンド版

```bash
# 1. Node ID取得
PARENT_NODE_ID=$(gh issue view $PARENT_ISSUE_ID --json id --jq '.id')
CHILD_NODE_ID=$(gh issue view $CHILD_ISSUE_ID --json id --jq '.id')

# 2. Sub-issue登録
gh api graphql \
  -H "GraphQL-Features: sub_issues" \
  -f "query=mutation {
    addSubIssue(input: {
      issueId: \"$PARENT_NODE_ID\",
      subIssueId: \"$CHILD_NODE_ID\"
    }) {
      issue { number }
      subIssue { number }
    }
  }" || true  # エラーでも続行
```

---

## エラーハンドリング

| エラー | 対応 |
|--------|------|
| Node ID取得失敗 | 処理をスキップ（警告ログ出力） |
| GraphQL API失敗 | 処理をスキップ（致命的エラーとしない） |
| ネットワークエラー | リトライ1回後スキップ |

**重要**: Sub-issue登録の失敗はワークフロー全体を停止させない。Issue自体は作成済みなので、手動でSub-issue関係を設定可能。

---

## 使用箇所

| ワークフロー | 用途 |
|-------------|------|
| `/decompose-issue` | 分割したSubtaskを親Issueに紐付け |
| `/detailed-design-workflow` | 作成したIssueをEpicに紐付け |

---

## CLIスクリプト

**自動化スクリプトが利用可能です：**

```bash
bash .opencode/skill/github-graphql-api/scripts/add-sub-issue.sh <parent-issue> <child-issue>
```

| 引数 | 説明 |
|------|------|
| `parent-issue` | 親Issue番号 |
| `child-issue` | Sub-issueとして追加するIssue番号 |

**使用例：**
```bash
bash .opencode/skill/github-graphql-api/scripts/add-sub-issue.sh 10 42
```
