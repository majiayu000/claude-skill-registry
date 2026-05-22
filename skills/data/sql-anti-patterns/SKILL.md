---
name: sql-anti-patterns
description: |
  SQLアンチパターンの検出・分析・改善提案を支援するスキル。
  スキーマ設計レビュー、クエリ実装レビュー、パフォーマンス問題の診断と改善を行う。

  Anchors:
  • SQL Antipatterns (Bill Karwin) / 適用: アンチパターンカタログ / 目的: 設計問題の体系的検出
  • Database Design for Mere Mortals / 適用: 正規化とスキーマ設計 / 目的: 適切なデータモデリング
  • Use The Index, Luke / 適用: インデックス最適化 / 目的: クエリパフォーマンス改善

  Trigger:
  Use when reviewing database schema, detecting SQL anti-patterns, diagnosing performance issues, or planning schema refactoring.
  sql anti-pattern, schema review, N+1, EAV, polymorphic associations, jaywalking, database design, query optimization
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# SQLアンチパターン検出・改善

## 概要

スキーマやクエリのアンチパターンを特定し、影響度と優先度を整理した上で、
改善案と移行計画を提示するスキル。

## ワークフロー

```
analyze-context → detect-patterns → evaluate-impact → plan-remediation → validate-changes
```

### Phase 1: コンテキスト分析

**目的**: 対象範囲と制約を整理する

**アクション**:

1. 対象DBとバージョン、運用環境を確認する
2. スキーマ定義（DDL、ORMスキーマ、ER図）を収集する
3. 問題のクエリやログ、実行計画を収集する
4. 目的と制約（性能目標、可用性、移行期間）を整理する

**Task**: `agents/context-analysis.md` を参照

### Phase 2: アンチパターン検出

**目的**: アンチパターンの候補を特定する

**アクション**:

1. `scripts/detect-anti-patterns.mjs` で自動検出を実行する
2. `references/anti-patterns-catalog.md` で候補の定義と症状を確認する
3. 直接の証拠がない指摘は「仮説」と明記する

**Task**: `agents/anti-pattern-detection.md` を参照

### Phase 3: 影響評価

**目的**: 検出されたパターンの影響度を評価する

**アクション**:

1. 影響度（性能/整合性/運用）を分析する
2. 移行コストを見積もる
3. 優先順位を決定する

**Task**: `agents/evaluate-impact.md` を参照

### Phase 4: 改善計画

**目的**: 具体的な改善案と移行計画を策定する

**アクション**:

1. 各アンチパターンに対する改善案を選定する
2. トレードオフを整理する
3. 移行・検証手順を策定する
4. `assets/schema-review-checklist.md` を記入する

**Task**: `agents/remediation-plan.md` を参照

## Task仕様ナビ

| Task                   | 起動タイミング | 入力                     | 出力               |
| ---------------------- | -------------- | ------------------------ | ------------------ |
| context-analysis       | Phase 1開始時  | DB情報、スキーマ、クエリ | コンテキスト整理書 |
| anti-pattern-detection | Phase 2開始時  | コンテキスト整理書       | 検出結果レポート   |
| evaluate-impact        | Phase 3開始時  | 検出結果レポート         | 影響評価レポート   |
| remediation-plan       | Phase 4開始時  | 影響評価レポート         | 改善計画書         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                     | 理由                       |
| ---------------------------- | -------------------------- |
| 証拠に基づいて指摘する       | 仮説と事実を明確に区別     |
| 例外条件を先に確認する       | 誤検出を避ける             |
| 影響度と移行コストを併記する | 優先順位判断の根拠を明確化 |
| 段階的な移行計画を策定する   | リスク分散と検証機会の確保 |
| テスト計画を含める           | 回帰バグの防止             |

### 避けるべきこと

| 禁止事項                       | 問題点                   |
| ------------------------------ | ------------------------ |
| 証拠なしの断定                 | 誤った判断を招く         |
| 一括移行の強行                 | 障害リスクが高い         |
| パフォーマンス計測なしの最適化 | 効果不明の作業になる     |
| 例外ケースの無視               | 正当なユースケースを壊す |
| 移行後の検証省略               | 問題の発見が遅れる       |

## リソース参照

### references/（詳細知識）

| リソース               | パス                                                                       | 読込条件       |
| ---------------------- | -------------------------------------------------------------------------- | -------------- |
| アンチパターンカタログ | [references/anti-patterns-catalog.md](references/anti-patterns-catalog.md) | パターン確認時 |

### scripts/（決定論的処理）

| スクリプト                 | 機能                   | 使用例                                           |
| -------------------------- | ---------------------- | ------------------------------------------------ |
| `detect-anti-patterns.mjs` | アンチパターン自動検出 | `node scripts/detect-anti-patterns.mjs <schema>` |
| `validate-skill.mjs`       | スキル構造検証         | `node scripts/validate-skill.mjs`                |

### assets/（テンプレート）

| アセット                     | 用途                           |
| ---------------------------- | ------------------------------ |
| `schema-review-checklist.md` | スキーマレビューチェックリスト |

## 変更履歴

| Version | Date       | Changes                                         |
| ------- | ---------- | ----------------------------------------------- |
| 2.0.0   | 2026-01-03 | 18-skills.md仕様に完全準拠、Anchors/Trigger追加 |
| 1.0.0   | 2025-12-28 | 初版作成                                        |
