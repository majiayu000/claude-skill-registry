---
name: docker-mcp-ops
description: |
  Docker MCPでコンテナ操作（起動/停止/ログ）を会話で実行。
  Use when: (1) user says「コンテナ起動」「Docker操作」「ログ確認」,
  (2) user wants container management via conversation,
  (3) user mentions「docker-compose」「サービス再起動」.
  Do NOT use for: Dockerファイル作成（一般開発）、
  セキュリティスキャン（security-scan-trivyを使用）。
---

# Docker MCP Ops

## Instructions

- 変更前に現状（ps/logs）を確認
- 影響範囲（依存サービス/ボリューム）を確認してから操作する

