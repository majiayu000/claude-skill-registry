---
name: workflow-automation-n8n
description: n8nで業務フローを設計・実装する。トリガー→処理→例外→通知まで一気通貫で提案する時に使う。
---

# n8n Workflow Automation

## Instructions

- 要件を「Trigger / Steps / Data / Error handling / Notification / Audit」に分解
- 最小ノード構成→拡張構成の順で提案
- 失敗時の再実行設計（冪等性）を必ず入れる

## Example

- Trigger: Webhook
- Steps: DB lookup → API call → Update DB
- Notification: 成功/失敗を統一通知

