---
name: handle-ci-failure
description: CI (GitHub Actions) の失敗を検知・分析し、LinearのIssueとして登録します
model: opus
---

CIの失敗を調査し、永続化（チケット化）します。

## 手順

1. **ステータス確認**:
   - `gh run list --limit 1 --json conclusion,workflowName,url` で直近の状況を確認。
   - `conclusion` が `failure` でなければ、「CIは成功しています」と報告して終了。

2. **ログ分析**:
   - `gh run view --log-failed` でエラーログを取得。
   - エラーの根本原因を特定する（Lint / Test / Build / Security）。
   - 必要に応じて `cat` で関連コードを確認。

3. **Linear Issue 起票（提案）**:
   - 以下の内容でLinearチケットを作成することをユーザーに提案（またはMCPで作成）:
     - **Title**: `CI Failure: [エラーの概要]` (例: `CI Failure: Vitest failed in UserAuth`)
     - **Description**:
       - 失敗したWorkflow: [WorkflowName]
       - ログ抜粋: (コードブロック)
       - 推定原因: ...
       - 関連URL: [PR or Run URL]
     - **Label**: `Bug`
     - **Priority**: `High`

4. **次のアクション提案**:
   - チケット作成後、ユーザーに以下を提案：
     - 「このまま修正作業（`fix`）に入りますか？」
     - 「それとも一旦チケット化だけして終了しますか？」

## 使いどころ
- CI失敗の通知が来た後に呼び出す。
- `review-flow` の前に、ビルドが通っているか確認するために呼び出す。
