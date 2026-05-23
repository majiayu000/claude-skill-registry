---
name: mcp-protocol
description: |
  Model Context Protocol (MCP) 仕様と実装パターン。サーバー設定、ツール定義、LLM統合向けJSONスキーマ設計を提供。

  Anchors:
  • MCP Official Specification / 適用: プロトコルバージョン、メッセージフォーマット / 目的: 仕様準拠
  • JSON Schema Draft-07 / 適用: inputSchemaバリデーション / 目的: 型安全ツール定義
  • The Pragmatic Programmer / 適用: DRY、直交性 / 目的: 保守性の高い設定

  Trigger:
  Use when configuring MCP servers, designing tool definitions with JSON Schema,
  validating MCP protocol compliance, or troubleshooting connection/timeout errors.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# MCP Protocol

> **相対パス**: `SKILL.md`
> **読込条件**: スキル使用時（自動）

---

## 概要

Model Context Protocol (MCP) の標準仕様と実装パターン。

**対象領域**:

| 領域             | 説明                               |
| ---------------- | ---------------------------------- |
| サーバー設定     | claude_mcp_config.json 構造        |
| ツール定義       | name, description, inputSchema     |
| プロトコル準拠   | バージョン、メッセージフォーマット |
| トラブルシュート | 接続エラー、タイムアウト対応       |

---

## ワークフロー

### Phase 1: 要件分析

**Task**: `agents/analyze-requirements.md`

| 入力             | 出力     |
| ---------------- | -------- |
| MCP サーバー要件 | 設計仕様 |

**参照**: `references/basics.md`

### Phase 2: サーバー設定

**Task**: `agents/configure-server.md`

| 入力     | 出力         |
| -------- | ------------ |
| 設計仕様 | 設定ファイル |

**参照**: `references/patterns.md`, `assets/`

### Phase 3: 検証

**Task**: `agents/validate-implementation.md`

| 入力         | 出力         |
| ------------ | ------------ |
| 設定ファイル | 検証レポート |

### Phase 4: トラブルシュート

**Task**: `agents/troubleshoot-issues.md`

| 入力       | 出力           |
| ---------- | -------------- |
| エラー情報 | 解決策レポート |

**参照**: `references/troubleshooting.md`

---

## ベストプラクティス

| すべきこと                           | 避けるべきこと               |
| ------------------------------------ | ---------------------------- |
| inputSchema で型安全なパラメータ定義 | スキーマなしのツール定義     |
| 明確な description を記述            | 曖昧なツール説明             |
| 環境変数で機密情報を管理             | ハードコードされた認証情報   |
| タイムアウト設定を適切に設定         | デフォルトタイムアウトの放置 |
| プロトコルバージョンを明示           | バージョン不整合の放置       |

---

## Task ナビゲーション

| Task                         | 目的             | 参照リソース          |
| ---------------------------- | ---------------- | --------------------- |
| `analyze-requirements.md`    | サーバー要件分析 | `basics.md`           |
| `configure-server.md`        | 設定ファイル生成 | `patterns.md`, assets |
| `validate-implementation.md` | 実装検証         | scripts               |
| `troubleshoot-issues.md`     | 問題解決         | `troubleshooting.md`  |

---

## リソース参照

### References

| ファイル               | 内容                         | 読込条件   |
| ---------------------- | ---------------------------- | ---------- |
| `basics.md`            | MCP 基礎概念・用語           | 初回使用時 |
| `patterns.md`          | ツール定義・設定パターン     | 設計時     |
| `mcp-specification.md` | プロトコル仕様詳細           | 仕様確認時 |
| `config-examples.md`   | 設定例集                     | 実装時     |
| `troubleshooting.md`   | トラブルシューティングガイド | 問題発生時 |

### Assets

| ファイル                        | 内容                     |
| ------------------------------- | ------------------------ |
| `server-config-template.json`   | サーバー設定テンプレート |
| `tool-definition-template.json` | ツール定義テンプレート   |

### Scripts

| スクリプト                 | 用途               |
| -------------------------- | ------------------ |
| `validate-mcp-config.mjs`  | MCP 設定検証       |
| `validate-tool-schema.mjs` | ツールスキーマ検証 |
| `log_usage.mjs`            | 使用記録           |

---

## 関連スキル

- `mcp-server-patterns` - MCP サーバー実装パターン
- `json-schema` - JSON Schema 設計
- `api-client-patterns` - API クライアントパターン
