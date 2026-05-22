---
name: query-performance-tuning
description: |
  SQLiteクエリパフォーマンス最適化を専門とするスキル。EXPLAIN QUERY PLAN分析、インデックス戦略、クエリリライトを通じて、遅いクエリを診断し実行計画を改善します。

  Anchors:
  • High Performance MySQL (Baron Schwartz) / 適用: クエリ分析と診断手法 / 目的: 体系的なパフォーマンス診断
  • Use The Index, Luke (Markus Winand) / 適用: インデックス設計原則 / 目的: 効果的なインデックス活用
  • Systems Performance (Brendan Gregg) / 適用: 測定駆動のアプローチ / 目的: 定量的な効果検証

  Trigger:
  Use when optimizing slow queries, analyzing execution plans, designing indexes, resolving N+1 problems, or improving database performance systematically.
  Keywords: slow query, EXPLAIN QUERY PLAN, index optimization, query rewriting, N+1 problem, database performance, SQLite performance
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Query Performance Tuning

## 概要

SQLiteクエリパフォーマンスを測定駆動で最適化します。遅いクエリの診断、実行計画の分析、インデックス設計、クエリリライトを段階的に実施し、パフォーマンス改善を実現します。

## ワークフロー

### Phase 1: Analysis（分析）

**目的**: 遅いクエリを特定し、実行計画を分析してボトルネックを診断

**Task**: `agents/analysis.md`

**入力**:

- 対象クエリ（SQL文）
- パフォーマンス要件（許容レスポンス時間）

**出力**:

- EXPLAIN QUERY PLAN 分析結果
- ボトルネック診断レポート
- 最適化の優先順位

**実行タイミング**: クエリが遅いと報告された時、パフォーマンス問題の調査時

### Phase 2: Optimization（最適化）

**目的**: インデックス設計、クエリリライト、N+1問題解決を実施

**Task**: `agents/optimization.md`

**入力**:

- Phase 1 の分析結果
- データベーススキーマ
- クエリパターン

**出力**:

- インデックス設計案（DDL含む）
- 最適化されたクエリ
- 実装手順書

**実行タイミング**: 分析後の改善実施、インデックス追加判断時

### Phase 3: Validation（検証）

**目的**: 最適化効果を測定し、パフォーマンス改善を検証

**Task**: `agents/validation.md`

**入力**:

- 最適化前後のクエリ
- ベンチマーク条件

**出力**:

- パフォーマンス比較レポート
- 改善率の測定結果
- 残存課題の特定

**実行タイミング**: 最適化実施後、効果測定が必要な時

## Task仕様

| Task         | 起動タイミング | 入力               | 出力                    |
| ------------ | -------------- | ------------------ | ----------------------- |
| analysis     | Phase 1開始時  | クエリ・要件       | ボトルネック診断        |
| optimization | Phase 2開始時  | 分析結果・スキーマ | インデックス・最適化SQL |
| validation   | Phase 3開始時  | 最適化前後クエリ   | 検証レポート            |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

- [agents/analysis.md](agents/analysis.md)
- [agents/optimization.md](agents/optimization.md)
- [agents/validation.md](agents/validation.md)

## ベストプラクティス

### すべきこと

- 測定から始める（推測による最適化を避ける）
- EXPLAIN QUERY PLAN で実行計画を必ず確認
- インデックス追加前にクエリパターンを分析
- N+1問題は早期に特定して解決
- 最適化効果を数値で検証
- 書き込み性能への影響を考慮

### 避けるべきこと

- 測定なしの盲目的なインデックス追加
- 実行計画を見ずにクエリを変更
- 過度なインデックス（書き込み性能の劣化）
- 単一クエリのみの最適化（全体像を見失う）
- 統計的妥当性のない測定

## リソース参照

### references/（詳細知識）

| リソース                   | パス                                                                       | 内容               |
| -------------------------- | -------------------------------------------------------------------------- | ------------------ |
| 基礎知識                   | [references/Level1_basics.md](references/Level1_basics.md)                 | 基礎概念と用語     |
| 実務パターン               | [references/Level2_intermediate.md](references/Level2_intermediate.md)     | 実務での適用       |
| 高度な最適化               | [references/Level3_advanced.md](references/Level3_advanced.md)             | 高度な最適化技法   |
| 専門トラブルシューティング | [references/Level4_expert.md](references/Level4_expert.md)                 | 専門的な問題解決   |
| EXPLAIN解析                | [references/explain-analyze-guide.md](references/explain-analyze-guide.md) | 実行計画の読解     |
| インデックス戦略           | [references/index-strategies.md](references/index-strategies.md)           | インデックス設計   |
| クエリパターン             | [references/query-patterns.md](references/query-patterns.md)               | 最適化パターン     |
| 監視クエリ                 | [references/monitoring-queries.md](references/monitoring-queries.md)       | パフォーマンス監視 |

### scripts/（決定論的処理）

| スクリプト                 | 用途           | 使用例                                                                       |
| -------------------------- | -------------- | ---------------------------------------------------------------------------- |
| `analyze-slow-queries.mjs` | 遅いクエリ分析 | `node scripts/analyze-slow-queries.mjs --query "SELECT ..." --threshold 100` |
| `log_usage.mjs`            | 使用履歴記録   | `node scripts/log_usage.mjs --result success --phase analysis`               |
| `validate-skill.mjs`       | 構造検証       | `node scripts/validate-skill.mjs`                                            |

### assets/（テンプレート）

| テンプレート                     | 用途                       |
| -------------------------------- | -------------------------- |
| `performance-report-template.md` | パフォーマンス分析レポート |

## 変更履歴

| Version | Date       | Changes                                                      |
| ------- | ---------- | ------------------------------------------------------------ |
| 3.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠: optimization/validation agents追加 |
| 2.1.0   | 2026-01-02 | Task仕様テーブル形式化                                       |
| 2.0.0   | 2025-12-31 | 18-skills.md 仕様に準拠、agents/ Task追加                    |
| 1.0.0   | 2025-12-24 | 初版                                                         |
