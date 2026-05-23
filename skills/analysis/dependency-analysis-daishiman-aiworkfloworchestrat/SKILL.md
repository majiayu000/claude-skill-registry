---
name: dependency-analysis
description: |
  依存関係の可視化、循環依存検出、安定度評価を体系化するスキル。
  アーキテクチャの健全性を測定し、改善優先度を整理する。

  Anchors:
  • Clean Architecture / 適用: 安定依存の原則 / 目的: 依存方向の評価
  • Refactoring / 適用: 依存解消パターン / 目的: 循環依存の改善
  • Graph Algorithms / 適用: 強連結成分 / 目的: 循環依存の検出

  Trigger:
  Use when analyzing module dependencies, detecting circular references, calculating stability metrics, or planning dependency refactoring.
  dependency graph, circular dependency, stability metrics, coupling, sdp violation
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# dependency-analysis

## 概要

依存関係の抽出から評価・改善提案までを一貫して支援し、保守性の高い構造を維持する。

## ワークフロー

### Phase 1: 依存関係整理

**目的**: 対象範囲と依存抽出条件を整理する。

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認する。
2. `assets/dependency-analysis-checklist.md` で要件を整理する。
3. `references/requirements-index.md` で要件整合を確認する。

**Task**: `agents/analyze-dependencies.md` を参照

### Phase 2: 循環依存評価

**目的**: 循環依存の検出と優先度を整理する。

**アクション**:

1. `scripts/analyze-dependencies.mjs` で依存グラフを生成する。
2. `references/circular-dependency.md` で解消方針を確認する。
3. 影響範囲を整理する。

**Task**: `agents/detect-cycles.md` を参照

### Phase 3: 安定度評価

**目的**: 安定度メトリクスを算出し、改善対象を整理する。

**アクション**:

1. `references/stability-metrics.md` で評価指標を確認する。
2. Ca/Ce と不安定度を計算する。
3. `assets/dependency-report.md` に結果を記録する。

**Task**: `agents/calculate-stability.md` を参照

### Phase 4: 可視化と検証

**目的**: 結果を可視化し、改善提案をまとめる。

**アクション**:

1. `assets/graph-visualization-template.md` で可視化形式を整理する。
2. `agents/visualize-graph.md` の観点で整理する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/visualize-graph.md` を参照

## Task仕様ナビ

| Task                 | 起動タイミング | 入力       | 出力                   |
| -------------------- | -------------- | ---------- | ---------------------- |
| analyze-dependencies | Phase 1開始時  | 対象範囲   | 依存抽出条件、要件メモ |
| detect-cycles        | Phase 2開始時  | 依存グラフ | 循環依存一覧、優先度   |
| calculate-stability  | Phase 3開始時  | 依存グラフ | 安定度レポート         |
| visualize-graph      | Phase 4開始時  | 分析結果   | 可視化コード、改善提案 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                 | 理由                 |
| ------------------------ | -------------------- |
| 依存抽出条件を明示する   | 誤検知を減らせる     |
| 循環依存の優先度を付ける | 改善順序が明確になる |
| 安定度を定量化する       | 説明責任を果たせる   |
| 可視化で共有する         | 合意形成がしやすい   |

### 避けるべきこと

| 禁止事項               | 問題点         |
| ---------------------- | -------------- |
| 依存グラフを放置する   | 改善が進まない |
| 優先度を付けない       | 効果が薄い     |
| メトリクスを記録しない | 追跡ができない |
| 可視化なしで共有       | 誤解が生まれる |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                         | 機能                         |
| ---------------------------------- | ---------------------------- |
| `scripts/analyze-dependencies.mjs` | 依存関係分析                 |
| `scripts/validate-skill.mjs`       | スキル構造検証               |
| `scripts/log_usage.mjs`            | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース     | パス                                                                   | 読込条件       |
| ------------ | ---------------------------------------------------------------------- | -------------- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)             | 要件整理時     |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 循環依存評価時 |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)         | 安定度評価時   |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)             | 検証時         |
| 循環依存     | [references/circular-dependency.md](references/circular-dependency.md) | 循環評価時     |
| 依存グラフ   | [references/dependency-graph.md](references/dependency-graph.md)       | 抽出時         |
| 安定度指標   | [references/stability-metrics.md](references/stability-metrics.md)     | 評価時         |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md)   | 仕様確認時     |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)               | 互換確認時     |

### assets/（テンプレート・素材）

| アセット                                  | 用途                   |
| ----------------------------------------- | ---------------------- |
| `assets/dependency-report.md`             | 分析レポート           |
| `assets/dependency-analysis-checklist.md` | 依存分析チェックリスト |
| `assets/graph-visualization-template.md`  | 可視化テンプレート     |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
