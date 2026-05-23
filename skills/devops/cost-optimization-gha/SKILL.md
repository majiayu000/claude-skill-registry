---
name: cost-optimization-gha
description: |
  GitHub Actions の実行コストを最適化するためのスキル。
  コスト計測、削減施策の設計、実装、継続的な監視を一連で扱う。

  Anchors:
  • High Performance Browser Networking / 適用: 計測から改善する姿勢 / 目的: 速度とコストの可視化
  • Designing Data-Intensive Applications / 適用: 制約下の設計判断 / 目的: ランナー/ストレージの効率化
  • Continuous Delivery / 適用: 改善の反復 / 目的: 継続的最適化のサイクル化

  Trigger:
  Use when optimizing GitHub Actions workflow execution time, reducing runner costs, managing billing, or optimizing artifact storage and cache usage.
  github actions cost optimization, runner costs, workflow budget, artifact storage, caching strategy
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# cost-optimization-gha

## 概要

GitHub Actions のコストを計測し、実行時間・ランナー単価・ストレージを最適化する。

## ワークフロー

### Phase 1: 現状把握

**目的**: 実行時間、コスト、ストレージのベースラインを把握する。

**アクション**:

1. 実行頻度とジョブ構成を整理する。
2. `scripts/estimate-costs.mjs` で概算コストを見積もる。
3. コスト要因（ランナー種別、マトリクス、アーティファクト）を洗い出す。

**Task**: `agents/analyze-cost-baseline.md` を参照

### Phase 2: 最適化設計

**目的**: 削減施策と優先順位を設計する。

**アクション**:

1. 優先順位と削減目標を決める。
2. ランナー選定・キャッシュ・ストレージ方針を整理する。
3. 影響範囲とリスクを評価する。

**Task**: `agents/design-cost-optimization.md` を参照

### Phase 3: 実装

**目的**: ワークフローを改善し、コスト削減を実装する。

**アクション**:

1. 変更点をワークフローに反映する。
2. キャッシュ、条件分岐、並列化を適用する。
3. 変更内容を記録する。

**Task**: `agents/implement-cost-controls.md` を参照

### Phase 4: 検証と運用

**目的**: 施策の効果を検証し、継続的に改善する。

**アクション**:

1. 実行時間・コスト・品質の変化を確認する。
2. `scripts/validate-skill.mjs` で構造を検証する。
3. `scripts/log_usage.mjs` で記録を残す。

**Task**: `agents/validate-cost-impact.md` を参照

## Task仕様ナビ

| Task                     | 起動タイミング | 入力                 | 出力                             |
| ------------------------ | -------------- | -------------------- | -------------------------------- |
| analyze-cost-baseline    | Phase 1開始時  | 現状の実行情報       | ベースラインメモ、コスト要因一覧 |
| design-cost-optimization | Phase 2開始時  | ベースラインメモ     | 最適化計画、優先順位表           |
| implement-cost-controls  | Phase 3開始時  | 最適化計画           | 改善済みワークフロー、変更記録   |
| validate-cost-impact     | Phase 4開始時  | 改善済みワークフロー | 検証レポート、運用ログ           |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                             | 理由                     |
| ------------------------------------ | ------------------------ |
| ベースラインを計測する               | 効果測定に必須           |
| ランナー種別を見直す                 | 単価差が大きい           |
| キャッシュを活用する                 | 実行時間を短縮できる     |
| アーティファクトの保持期間を管理する | ストレージコストを抑える |
| 実行頻度を最適化する                 | 無駄な実行を減らす       |

### 避けるべきこと

| 禁止事項             | 問題点             |
| -------------------- | ------------------ |
| コスト計測なしの変更 | 効果が判断できない |
| ランナー種別の固定化 | 最適化余地を失う   |
| キャッシュ未使用     | 実行時間が伸びる   |
| 変更記録を残さない   | 再現性が失われる   |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                   | 機能                         |
| ---------------------------- | ---------------------------- |
| `scripts/estimate-costs.mjs` | ワークフローコストの概算     |
| `scripts/validate-skill.mjs` | スキル構造の検証             |
| `scripts/log_usage.mjs`      | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース       | パス                                                                   | 読込条件       |
| -------------- | ---------------------------------------------------------------------- | -------------- |
| レベル1 基礎   | [references/Level1_basics.md](references/Level1_basics.md)             | 初回整理時     |
| レベル2 実務   | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 施策設計時     |
| レベル3 応用   | [references/Level3_advanced.md](references/Level3_advanced.md)         | 実装検討時     |
| レベル4 専門   | [references/Level4_expert.md](references/Level4_expert.md)             | 運用改善時     |
| ランナー単価   | [references/runner-costs.md](references/runner-costs.md)               | ランナー選定時 |
| 実行時間最適化 | [references/execution-time.md](references/execution-time.md)           | 時間短縮検討時 |
| ストレージ管理 | [references/artifact-storage.md](references/artifact-storage.md)       | 保持期間設計時 |
| 請求監視       | [references/billing-monitoring.md](references/billing-monitoring.md)   | 監視設定時     |
| 要求仕様索引   | [references/requirements-index.md](references/requirements-index.md)   | 仕様確認時     |
| 旧スキル       | [references/legacy-skill.md](references/legacy-skill.md)               | 互換確認時     |

### assets/（テンプレート・素材）

| アセット                            | 用途                   |
| ----------------------------------- | ---------------------- |
| `assets/optimized-workflow.yaml`    | 最適化ワークフロー例   |
| `assets/cost-optimization-plan.md`  | 最適化計画テンプレート |
| `assets/runner-selection-matrix.md` | ランナー選定マトリクス |
| `assets/cost-report-template.md`    | コスト検証レポート     |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
