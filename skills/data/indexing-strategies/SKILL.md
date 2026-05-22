---
name: indexing-strategies
description: |
  SQLiteにおけるインデックス設計戦略の専門知識。
  B-Treeインデックス、部分インデックス、式インデックス、カバリングインデックスの特性と選択基準を提供。
  Turso + Drizzle ORM環境での実装を前提とする。

  Anchors:
  • Designing Data-Intensive Applications (Martin Kleppmann) / 適用: データモデリング・インデックス設計原則 / 目的: 体系的なインデックス戦略の確立
  • SQLite Documentation / 適用: B-Tree実装・クエリプランナー挙動 / 目的: SQLite特有の最適化技法の適用
  • Drizzle ORM / 適用: index()構文・マイグレーション / 目的: 型安全なスキーマ定義

  Trigger:
  Use when designing database indexes, analyzing query performance, optimizing read operations, evaluating index candidates, or implementing Drizzle ORM index migrations.
  Keywords: index, indexing, B-Tree, query performance, SQLite, Drizzle, cardinality, selectivity, covering index, partial index, expression index.
version: 2.0.0
---

# Indexing Strategies Skill

## 概要

SQLiteのインデックス設計に関する専門知識を提供し、クエリパターンとデータ特性に基づいて最適なインデックス戦略を選択・設計します。

## ワークフロー

本スキルは3つのPhaseで構成されます。各Phaseは対応するTaskで実行されます。

### Phase 1: インデックス要件分析

**目的**: クエリパターンとデータ特性を分析し、インデックス候補を特定する

**Task**: [agents/analyze-index-requirements.md](agents/analyze-index-requirements.md)

**入力**:

- テーブルスキーマ情報（Drizzle ORM定義）
- クエリパターン（頻繁に実行されるクエリ）
- データ量とカーディナリティ情報

**出力**:

- クエリパターン分析結果
- カーディナリティ評価
- インデックス候補リスト
- パフォーマンス要件

**参照リソース**:

- [references/Level1_basics.md](references/Level1_basics.md) - インデックス基礎
- [references/index-types-comparison.md](references/index-types-comparison.md) - タイプ別特性

### Phase 2: インデックス戦略設計

**目的**: 具体的なインデックス設計を作成し、Drizzle ORM形式でマイグレーションコードを提供する

**Task**: [agents/design-index-strategy.md](agents/design-index-strategy.md)

**入力**:

- Phase 1の分析結果

**出力**:

- インデックス設計詳細
- Drizzle ORM マイグレーションコード
- トレードオフ分析（書き込みコスト vs 読み取り効果）

**参照リソース**:

- [references/Level2_intermediate.md](references/Level2_intermediate.md) - 実務ガイド
- [references/index-types-comparison.md](references/index-types-comparison.md) - タイプ選択基準
- [assets/index-design-checklist.md](assets/index-design-checklist.md) - 設計チェックリスト

### Phase 3: インデックス設計検証

**目的**: 設計の妥当性を検証し、実装前の最終チェックと記録を実施する

**Task**: [agents/validate-index-design.md](agents/validate-index-design.md)

**入力**:

- Phase 2の設計詳細

**出力**:

- 検証結果レポート
- 改善提案（問題がある場合）
- 使用記録（LOGS.mdへ自動記録）

**参照リソース**:

- [references/Level3_advanced.md](references/Level3_advanced.md) - 検証技法
- [assets/index-design-checklist.md](assets/index-design-checklist.md) - 最終チェックリスト

**スクリプト**:

- `scripts/analyze-indexes.mjs` - 既存インデックス分析、重複検出
- `scripts/log_usage.mjs` - 使用記録の自動保存

## Task仕様ナビゲーション

| Task                          | Phase | 役割     | 入力             | 出力               |
| ----------------------------- | ----- | -------- | ---------------- | ------------------ |
| analyze-index-requirements.md | 1     | 要件分析 | スキーマ・クエリ | インデックス候補   |
| design-index-strategy.md      | 2     | 戦略設計 | 分析結果         | 設計詳細・コード   |
| validate-index-design.md      | 3     | 設計検証 | 設計詳細         | 検証結果・改善提案 |

## ベストプラクティス

### すべきこと

- 新規テーブル作成時にインデックス戦略を事前設計する
- クエリパフォーマンス問題発生時に体系的に分析する
- インデックス追加前に必ずトレードオフを評価する
- JSON検索には式インデックスを検討する
- 複合インデックスでは選択性の高いカラムを先頭に配置する

### 避けるべきこと

- すべてのカラムにインデックスを作成する（書き込みコスト増大）
- 既存インデックスとの重複を確認せずに追加する
- カーディナリティが低いカラム（性別、ブール値など）に単独インデックスを作成する
- トレードオフを文書化せずに実装する

## リソース参照

### 段階的学習（Progressive Disclosure）

- **Level 1 (Basics)**: [references/Level1_basics.md](references/Level1_basics.md)
  - スキル適用タイミングと基本概念
- **Level 2 (Intermediate)**: [references/Level2_intermediate.md](references/Level2_intermediate.md)
  - 実務での判断基準と設計パターン
- **Level 3 (Advanced)**: [references/Level3_advanced.md](references/Level3_advanced.md)
  - 検証技法とパフォーマンス測定
- **Level 4 (Expert)**: [references/Level4_expert.md](references/Level4_expert.md)
  - 高度な最適化技法とエッジケース

### 詳細リソース

- **インデックスタイプ比較**: [references/index-types-comparison.md](references/index-types-comparison.md)
  - B-Tree、式、部分、カバリングインデックスの特性と選択基準
- **設計チェックリスト**: [assets/index-design-checklist.md](assets/index-design-checklist.md)
  - インデックス設計時の必須確認項目
- **旧仕様**: [references/legacy-skill.md](references/legacy-skill.md)
  - 以前のSKILL.md全文（参考資料）

## スクリプト

### analyze-indexes.mjs

既存インデックスの使用状況を分析し、未使用・重複インデックスを検出します。

```bash
node scripts/analyze-indexes.mjs [database-path]
```

### log_usage.mjs

スキル使用履歴を自動記録し、評価メトリクスを更新します。

```bash
node scripts/log_usage.mjs --result success --phase "validate-index-design"
```

### validate-skill.mjs

スキル構造がspec準拠であることを検証します。

```bash
node scripts/validate-skill.mjs
```

## 変更履歴

| Version | Date       | Changes                                                  |
| ------- | ---------- | -------------------------------------------------------- |
| 2.0.0   | 2025-12-24 | Spec alignment, Task仕様追加、Progressive Disclosure対応 |
| 1.0.0   | -          | 初版作成                                                 |
