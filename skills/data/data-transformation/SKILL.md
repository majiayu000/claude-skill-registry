---
name: data-transformation
description: |
  データ変換パイプラインの設計・実装・検証を整理するスキル。
  スキーママッピング、ETL設計、品質確認までの実務フローを提供する。

  Anchors:
  • Designing Data-Intensive Applications / 適用: データモデリング / 目的: 変換の整合性確保
  • Designing Data-Intensive Applications / 適用: スキーマ設計 / 目的: マッピングの明確化
  • Designing Data-Intensive Applications / 適用: パイプライン設計 / 目的: 伸縮性と監視性の確保

  Trigger:
  Use when designing data transformation pipelines, defining schema mappings, implementing ETL processes, or optimizing data flows.
  data transformation, schema mapping, etl design, pipeline optimization, data modeling
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# data-transformation

## 概要

データ変換の要件整理から設計・実装・検証までを一貫して支援し、堅牢な変換パイプラインを構築する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 入出力・制約・品質要件を整理する。

**アクション**:

1. 入出力データと目的を整理する。
2. 品質要件と許容遅延を確認する。
3. 変換ステップの候補を洗い出す。

**Task**: `agents/analyze-transformation-requirements.md` を参照

### Phase 2: 設計

**目的**: スキーママッピングとパイプライン構成を設計する。

**アクション**:

1. `references/schema-mapping-guide.md` でマッピング方針を確認する。
2. `references/etl-design-patterns.md` でETL設計を整理する。
3. 変換フローと検証点を定義する。

**Task**: `agents/design-transformation-architecture.md` を参照

### Phase 3: 実装

**目的**: 変換処理を実装し、品質チェックを組み込む。

**アクション**:

1. `assets/etl-pipeline-template.md` を参照して実装する。
2. `scripts/analyze-transformations.mjs` で変換点を確認する。
3. 変更点を記録する。

**Task**: `agents/implement-transformation-pipeline.md` を参照

### Phase 4: 検証と運用

**目的**: 変換品質を検証し、運用記録を残す。

**アクション**:

1. `assets/transformation-validation-checklist.md` で検証する。
2. `scripts/log_usage.mjs` で記録を更新する。
3. 改善点を整理する。

**Task**: `agents/validate-transformation-quality.md` を参照

## Task仕様ナビ

| Task                                | 起動タイミング | 入力       | 出力                       |
| ----------------------------------- | -------------- | ---------- | -------------------------- |
| analyze-transformation-requirements | Phase 1開始時  | 入出力情報 | 要件メモ、制約一覧         |
| design-transformation-architecture  | Phase 2開始時  | 要件メモ   | マッピング設計、フロー定義 |
| implement-transformation-pipeline   | Phase 3開始時  | 設計方針   | 実装メモ、変更点           |
| validate-transformation-quality     | Phase 4開始時  | 実装メモ   | 検証レポート、改善提案     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                   | 理由                   |
| -------------------------- | ---------------------- |
| 入出力スキーマを明確にする | 変換の整合性を保つ     |
| 検証ポイントを定義する     | 早期検知につながる     |
| 変換ステップを分割する     | 再利用と保守性が高まる |
| ログとメトリクスを残す     | 運用改善に役立つ       |

### 避けるべきこと

| 禁止事項           | 問題点               |
| ------------------ | -------------------- |
| スキーマ無しの変換 | データ破損リスク     |
| 例外処理の欠落     | 失敗時の影響が大きい |
| 変更履歴の未記録   | 再現性が失われる     |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                            | 機能                         |
| ------------------------------------- | ---------------------------- |
| `scripts/analyze-transformations.mjs` | 変換ポイントの分析           |
| `scripts/validate-skill.mjs`          | スキル構造の検証             |
| `scripts/log_usage.mjs`               | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース           | パス                                                                     | 読込条件   |
| ------------------ | ------------------------------------------------------------------------ | ---------- |
| レベル1 基礎       | [references/Level1_basics.md](references/Level1_basics.md)               | 要件整理時 |
| レベル2 実務       | [references/Level2_intermediate.md](references/Level2_intermediate.md)   | 設計時     |
| レベル3 応用       | [references/Level3_advanced.md](references/Level3_advanced.md)           | 実装時     |
| レベル4 専門       | [references/Level4_expert.md](references/Level4_expert.md)               | 検証時     |
| スキーママッピング | [references/schema-mapping-guide.md](references/schema-mapping-guide.md) | 設計時     |
| ETL設計            | [references/etl-design-patterns.md](references/etl-design-patterns.md)   | 設計時     |
| 品質評価           | [references/data-quality-metrics.md](references/data-quality-metrics.md) | 検証時     |
| 要求仕様索引       | [references/requirements-index.md](references/requirements-index.md)     | 仕様確認時 |
| 旧スキル           | [references/legacy-skill.md](references/legacy-skill.md)                 | 互換確認時 |

### assets/（テンプレート・素材）

| アセット                                        | 用途                         |
| ----------------------------------------------- | ---------------------------- |
| `assets/etl-pipeline-template.md`               | パイプライン設計テンプレート |
| `assets/schema-mapping-template.md`             | スキーママッピング整理       |
| `assets/transformation-validation-checklist.md` | 検証チェックリスト           |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
