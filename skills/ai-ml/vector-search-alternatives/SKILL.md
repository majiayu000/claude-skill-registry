---
name: vector-search-alternatives
description: |
  SQLiteプロジェクト向けのベクトル検索代替戦略スキル。
  SQLite VSS、外部ベクトルDB、RAGパイプラインの実装を提供します。

  Anchors:
  - The Pragmatic Programmer（Andrew Hunt）/ 適用: 実践的ソリューション選定 / 目的: 適材適所の技術選択
  - Designing Data-Intensive Applications（Martin Kleppmann）/ 適用: データシステム設計 / 目的: スケーラブルなアーキテクチャ
  - Building LLM Apps（各種論文）/ 適用: RAGパターン / 目的: 効果的な情報検索

  Trigger:
  Use when implementing vector search, building RAG systems, setting up SQLite VSS, or integrating external vector databases like Pinecone or Weaviate.

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Vector Search Alternatives

## 概要

SQLiteベースプロジェクト向けのベクトル検索実装代替戦略スキル。pgvectorが使えない環境で、SQLite VSS拡張、外部ベクトルDB、RAGパイプラインなど複数のアプローチを提供します。4つの専門エージェントによる包括的な実装支援を行います。

## エージェント構成

| エージェント           | 役割               | 主な機能                           |
| ---------------------- | ------------------ | ---------------------------------- |
| solution-selector      | ソリューション選定 | 要件分析、候補評価、推奨提案       |
| sqlite-vss-implementer | SQLite VSS実装     | スキーマ設計、インデックス最適化   |
| external-db-integrator | 外部ベクトルDB連携 | Pinecone/Weaviate/Qdrant統合       |
| rag-architect          | RAGシステム設計    | パイプライン設計、チャンキング戦略 |

## ワークフロー

### Phase 1: ソリューション選定

**目的**: プロジェクト要件に最適なベクトル検索アプローチを決定

**アクション**:

1. `solution-selector` で要件を分析
2. データ規模・パフォーマンス要件を評価
3. 推奨ソリューションを決定

### Phase 2: 実装

**目的**: 選定したソリューションを実装

**アクション**:

1. SQLite VSS → `sqlite-vss-implementer` を使用
2. 外部ベクトルDB → `external-db-integrator` を使用
3. RAGパイプライン → `rag-architect` を使用

### Phase 3: 検証と最適化

**目的**: 実装の検証とパフォーマンス最適化

**アクション**:

1. `scripts/benchmark-vector-search.mjs` でベンチマーク
2. `scripts/validate-skill.mjs` で構造検証
3. `scripts/log_usage.mjs` で使用記録

## Task仕様ナビ

| タスク              | 担当エージェント       | 参照リソース          |
| ------------------- | ---------------------- | --------------------- |
| ソリューション比較  | solution-selector      | `vector-basics.md`    |
| SQLite VSS実装      | sqlite-vss-implementer | `index-strategies.md` |
| Pinecone連携        | external-db-integrator | `vector-basics.md`    |
| RAGパイプライン構築 | rag-architect          | `rag-patterns.md`     |
| チャンキング最適化  | rag-architect          | `rag-patterns.md`     |

## ベストプラクティス

### すべきこと

- 小〜中規模（10万ベクトル以下）は**SQLite VSS**を第一候補にする
- 本番環境で高可用性が必要な場合は**外部ベクトルDB**を検討
- RAGシステムは**チャンキング戦略**を慎重に設計する
- `scripts/benchmark-vector-search.mjs` でパフォーマンスを定期的に測定

### 避けるべきこと

- 要件を分析せずにソリューションを選定すること
- インデックス設定を最適化せずに本番稼働すること
- エンベディングモデルのコスト・品質トレードオフを無視すること
- 障害時のフォールバック戦略を設計しないこと

## リソース参照

### エージェント

| エージェント                       | 説明               |
| ---------------------------------- | ------------------ |
| `agents/solution-selector.md`      | ソリューション選定 |
| `agents/sqlite-vss-implementer.md` | SQLite VSS実装     |
| `agents/external-db-integrator.md` | 外部ベクトルDB連携 |
| `agents/rag-architect.md`          | RAGシステム設計    |

### リファレンス

| リソース                         | 説明             |
| -------------------------------- | ---------------- |
| `references/vector-basics.md`    | ベクトル検索基礎 |
| `references/index-strategies.md` | インデックス戦略 |
| `references/rag-patterns.md`     | RAGパターン集    |

### アセット

| アセット                           | 説明                         |
| ---------------------------------- | ---------------------------- |
| `assets/vector-schema-template.ts` | ベクトルスキーマテンプレート |

### スクリプト

| スクリプト                            | 説明           | 使用方法                                          |
| ------------------------------------- | -------------- | ------------------------------------------------- |
| `scripts/benchmark-vector-search.mjs` | ベンチマーク   | `node scripts/benchmark-vector-search.mjs --help` |
| `scripts/validate-skill.mjs`          | スキル構造検証 | `node scripts/validate-skill.mjs -v`              |
| `scripts/log_usage.mjs`               | 使用記録       | `node scripts/log_usage.mjs`                      |

## 変更履歴

| バージョン | 日付       | 変更内容                                      |
| ---------- | ---------- | --------------------------------------------- |
| 2.0.0      | 2026-01-01 | 4エージェント体制への再構成、18-skills.md準拠 |
| 1.0.0      | 2025-12-24 | 初版リリース                                  |
