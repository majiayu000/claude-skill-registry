---
name: database-monitoring
description: |
  データベース監視の設計・実装・検証を体系化するスキル。
  SQLite/Tursoの統計情報、スロークエリ、接続数、ストレージを含めた監視運用を整理する。

  Anchors:
  • Designing Data-Intensive Applications / 適用: 性能とスケーリング設計 / 目的: 監視メトリクスの根拠整理
  • Database Reliability Engineering / 適用: SREの監視設計 / 目的: 監視項目の体系化
  • Observability / 適用: 監視と診断 / 目的: 可観測性の向上

  Trigger:
  Use when designing database monitoring metrics, alert thresholds, SLI/SLOs, or operational dashboards for SQLite/Turso.
  database monitoring, sqlite metrics, turso monitoring, slow query, alerting, sli slo
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# database-monitoring

## 概要

SQLite/Turso を中心に、監視項目の選定・アラート設計・ダッシュボード設計を整理し、運用で使える監視設計を提供する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 監視対象と品質要件を整理する。

**アクション**:

1. 監視対象DBと用途を整理する。
2. 重要なSLI/SLOとアラート目的を明確化する。
3. 監視対象の優先度を整理する。

**Task**: `agents/analyze-monitoring-requirements.md` を参照

### Phase 2: 設計

**目的**: メトリクスとアラートの設計を行う。

**アクション**:

1. `references/health-metrics.md` で監視指標を整理する。
2. `references/alerting-strategies.md` でアラート設計を確認する。
3. ダッシュボード構成を決める。

**Task**: `agents/design-monitoring-architecture.md` を参照

### Phase 3: 実装

**目的**: 監視の初期実装を行い、ログを整備する。

**アクション**:

1. `scripts/connection-stats.mjs` と `scripts/health-check.mjs` を実行する。
2. `assets/alert-rules-template.md` を使ってアラートを定義する。
3. 変更点を記録する。

**Task**: `agents/implement-monitoring-setup.md` を参照

### Phase 4: 検証と運用

**目的**: 監視の品質を検証し、運用記録を残す。

**アクション**:

1. `assets/monitoring-review-checklist.md` で検証する。
2. `references/slow-query-logging.md` で改善点を確認する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-monitoring-quality.md` を参照

## Task仕様ナビ

| Task                            | 起動タイミング | 入力          | 出力                         |
| ------------------------------- | -------------- | ------------- | ---------------------------- |
| analyze-monitoring-requirements | Phase 1開始時  | 監視対象/要件 | 監視要件メモ、優先度一覧     |
| design-monitoring-architecture  | Phase 2開始時  | 要件メモ      | メトリクス設計、アラート設計 |
| implement-monitoring-setup      | Phase 3開始時  | 設計方針      | 設定メモ、初期検証結果       |
| validate-monitoring-quality     | Phase 4開始時  | 設定メモ      | 検証レポート、改善提案       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                   | 理由                     |
| -------------------------- | ------------------------ |
| 監視目的を明確にする       | アラートの精度が上がる   |
| SLI/SLOを先に決める        | 閾値設計が容易になる     |
| スロークエリを継続監視する | 性能劣化を早期検知できる |
| ダッシュボードを要約する   | 運用判断が迅速になる     |

### 避けるべきこと

| 禁止事項           | 問題点               |
| ------------------ | -------------------- |
| 目的のない指標追加 | ノイズが増える       |
| 閾値の過小設定     | アラート疲れが起きる |
| 記録の欠落         | 改善ができない       |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                     | 機能                         |
| ------------------------------ | ---------------------------- |
| `scripts/connection-stats.mjs` | 接続統計取得                 |
| `scripts/health-check.mjs`     | 健全性チェック               |
| `scripts/validate-skill.mjs`   | スキル構造の検証             |
| `scripts/log_usage.mjs`        | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース     | パス                                                                   | 読込条件       |
| ------------ | ---------------------------------------------------------------------- | -------------- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)             | 要件整理時     |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 設計時         |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)         | 実装時         |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)             | 検証時         |
| 健全性指標   | [references/health-metrics.md](references/health-metrics.md)           | 指標選定時     |
| アラート設計 | [references/alerting-strategies.md](references/alerting-strategies.md) | アラート設計時 |
| スロークエリ | [references/slow-query-logging.md](references/slow-query-logging.md)   | 改善時         |
| SQLite統計   | [references/sqlite-statistics.md](references/sqlite-statistics.md)     | 指標確認時     |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md)   | 仕様確認時     |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)               | 互換確認時     |

### assets/（テンプレート・素材）

| アセット                                     | 用途                       |
| -------------------------------------------- | -------------------------- |
| `assets/alert-rules-template.md`             | アラート定義テンプレート   |
| `assets/monitoring-dashboard-template.md`    | ダッシュボードテンプレート |
| `assets/monitoring-requirements-template.md` | 監視要件整理               |
| `assets/monitoring-review-checklist.md`      | 検証チェックリスト         |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
