---
name: postgres-mcp-analyst
description: |
  PostgreSQL MCPでスキーマ確認とread-only分析を実行。
  Use when: (1) user says「DB分析」「SQLで集計」「PostgresSQL確認」,
  (2) user wants database analysis or reports,
  (3) user mentions「意思決定資料」「データ集計」「スキーマ確認」.
  Do NOT use for: DB更新・書き込み操作、マイグレーション。
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# PostgreSQL MCP Analyst

## Instructions

- 目的→必要指標→必要テーブル→クエリ案→検証（read-only）
- 大量取得を避け、集計/絞り込み/LIMITを優先
- 結果は「数値」「解釈」「次アクション」に落とす

